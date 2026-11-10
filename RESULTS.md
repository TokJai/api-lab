# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: "A Tender Quattro Stagioni"
- Step 0.12, results of the three runs without a session (optional): Run 1: PASSED, Run 2: PASSED, Run 3: FAILED (assert 401 == 200)
- Step 0.16, blocks of "how many of the three tools are excluded":
  - Block 1 (0 tools excluded): `[]`
  - Block 2 (1 tool excluded): `["Knife"]`, `["Scissors"]`, `["Pizza cutter"]`
  - Block 3 (2 tools excluded): `["Knife", "Scissors"]`
  - Block 4 (3 tools excluded - all tools): `["Knife", "Pizza cutter", "Scissors"]`

## Defect report
- Title: Server returns 500 Internal Server Error when all pizza tools are excluded
- Request: `POST https://quickpizza.grafana.com/api/pizza` with header `Authorization: token <token>` and body `{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}`
- Expected result: HTTP 400 Bad Request with a JSON error message explaining that no pizza can satisfy the request (e.g. `{"error": "no pizza satisfies tool constraints"}`)
- Actual result: HTTP 500 Internal Server Error with empty body (`Content-Length: 0`)
- Severity: Medium (Internal server exception caused by unhandled domain constraint, causing crash response rather than graceful validation error)

## Part A
- Step A4, status codes when the other user reads, changes and deletes:
  - Read (GET): 404
  - Change (PUT): 400
  - Delete (DELETE): 400

## Part B
1. **Kinds of failures and Unit testing comparison:**
   - Two kinds of failures that API tests can find but unit tests with stubs cannot:
     - *Unfaithful doubles / Contract mismatches:* When backend schema, routes, status codes, or serialization formats change, stubs based on outdated assumptions continue passing, while API integration tests catch the mismatch against the actual running service.
     - *Integration and environment issues:* Real communication failures across architectural boundaries, such as load balancer session routing (cookie persistence), database constraint violations, network latency/timeouts, and authentication middleware interactions.
   - One reason to write unit tests with stubs as well:
     - Unit tests are fast, deterministic, hermetic, and pinpoint the exact failing line or function immediately without depending on network availability or external service state. They provide an immediate feedback loop during development.

2. **User creation per test vs Public token:**
   - Every test creates its own user with a unique name (`lab-<uuid>`) to achieve test isolation. Because QuickPizza is a shared environment accessed concurrently by multiple users, using a shared token would cause tests to overwrite, modify, or delete each other's ratings, creating flaky and order-dependent tests.
   - In Project 2 (shared shop or hotel), we will apply the same principle by ensuring tests create independent test entities (such as unique customer usernames, reservations, or cart items prefixed with timestamps/UUIDs) and clean them up afterwards, rather than mutating shared global data.

3. **Shared Session and Step 0.12 observations:**
   - The QuickPizza system operates across multiple backend servers behind an AWS Application Load Balancer. User accounts created on one backend instance are stored locally on that instance. A single `requests.Session` retains and returns the `AWSALB` / `AWSALBCORS` cookies, maintaining sticky sessions so that subsequent login and rating requests hit the exact same backend server.
   - In Step 0.12, running requests independently without a session resulted in:
     - Run 1: PASSED
     - Run 2: PASSED
     - Run 3: FAILED (`401 Unauthorized` during login because the load balancer routed the request to a different server instance that had no record of the new user).

4. **Excluded tools defect analysis and xfail usage:**
   - The block of *3 tools excluded (all tools)* (`["Knife", "Pizza cutter", "Scissors"]`) revealed the defect.
   - A 500 Internal Server Error with an empty body is worse because it indicates an unhandled server crash, offering zero diagnostic feedback to the client application and preventing meaningful error messages for end users. A 400 Bad Request with a clear JSON error body informs the caller why the request was rejected.
   - The test remains in the suite with `@pytest.mark.xfail(..., strict=True)` rather than being deleted so that the defect is tracked in regression testing. With `strict=True`, the test suite remains green today, but as soon as the developers fix the defect, the test will fail (unexpectedly pass), alerting the QA team to update the assertion and remove the xfail marker.

5. **Base Choice Coverage vs All Combinations Coverage:**
   - Characteristics and blocks from Step A1:
     - C1: Value of stars = 3 blocks (below 1, 1 to 5 [base], above 5)
     - C2: Type of stars = 4 blocks (whole number [base], decimal, text, missing)
     - C3: Pizza = 2 blocks (exists [base], does not exist)
     - C4: Token = 3 blocks (user's own [base], none, wrong length)
   - *Base Choice Coverage:* 1 base test + non-base blocks of each characteristic held at base:
     $$1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 1 + 2 + 3 + 1 + 2 = 9\text{ tests}$$
   - *All Combinations Coverage:* Cartesian product of all blocks:
     $$3 \times 4 \times 2 \times 3 = 72\text{ tests}$$

6. **Status codes in Step A4 and inconsistency defect:**
   - In Step A4, we observed:
     - Read (GET): `404 Not Found` (`{"error": "not found"}`)
     - Change (PUT): `400 Bad Request` (`{"error": "rating ID <id> not found"}`)
     - Delete (DELETE): `400 Bad Request` (`{"error": "rating ID <id> not found"}`)
   - Expected status codes: We expect `403 Forbidden` (authenticated, but forbidden to access/modify resources owned by another user) or `404 Not Found` (to avoid leaking resource existence to strangers).
   - Is it a defect? Yes. Returning `400 Bad Request` for PUT and DELETE is an API defect because 400 implies client syntax errors, yet the server message explicitly states the resource is "not found" (which should be 404 or 403). Furthermore, returning 404 for GET but 400 for PUT/DELETE on the same unauthorized condition demonstrates poor API consistency.

7. **Arbitrary 16-character Token (`madeup.txt`):**
   - Running `curl -H "@madeup.txt" https://quickpizza.grafana.com/api/ratings` returned `HTTP 200 OK` and a full list of ratings from across the system.
   - This is a critical security vulnerability (Broken Authentication / Insecure Token Validation). The API server only verifies that the Authorization header contains any 16-character string rather than validating a cryptographically verified token or authenticating active sessions.
   - On a real system, an unauthorized stranger could generate random 16-character tokens to bypass authentication, harvest user data, spy on customer activity, and compromise system privacy.

8. **API Testing vs Web Page (UI) Testing:**
   - *One thing API tests check better:* Fast, deterministic verification of backend contracts, precise status codes, headers, and JSON schemas, including edge cases and bypass testing (sending payloads that bypass frontend client restrictions).
   - *One thing only web tests can check:* The complete end-to-end user experience, graphical rendering, CSS styles, responsive layouts, client-side JavaScript execution, and UI usability as directly perceived by the user.
