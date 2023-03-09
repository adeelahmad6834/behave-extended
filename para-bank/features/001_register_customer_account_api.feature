@api
Feature: 001 Register Customer Account on Parabank

  Scenario: 1.1 - A new user can access the homepage of Parabank.
    Given the user has a public endpoint to visit homepage of parabank.
    When the user makes the "GET" request to the endpoint.
    Then the request passes with the status code "200".
    And the user receives a "JSESSIONID" as a token.

  Scenario: 1.2 - A new user can access the registration page of Parabank with a valid JSESSIONID.
    Given the user has already visited the homepage of parabank.
    And the user has "a valid" JSESSIONID as a token.
    And the user has a public endpoint to visit the registration page of Parabank.
    When the user makes the "GET" request to the endpoint.
    Then the request passes with the status code "200".

  Scenario: 1.3 - A new user can still access the registration page of Parabank with an invalid JSESSIONID.
    Given the user has already visited the homepage of parabank.
    And the user has "an invalid" JSESSIONID as a token.
    And the user has a public endpoint to visit the registration page of Parabank.
    When the user makes the "GET" request to the endpoint.
    Then the request passes with the status code "200".

  Scenario: 1.4 - A new user can register as a customer by providing valid details and a valid JSESSIONID.
    Given the user has already visited the registration page of parabank with "a valid" JSESSIONID.
    And the user has a public endpoint to register a customer account.
    And the user has a payload for account registration.
    When the user makes the "POST" request to the endpoint.
    Then the request passes with the status code "200".
    And the customer account is registered successfully.

  Scenario: 1.5 - A new user can not register as a customer by providing valid details and an invalid JSESSIONID.
    Given the user has already visited the registration page of parabank with "an invalid" JSESSIONID.
    And the user has a public endpoint to register a customer account.
    And the user has a payload for account registration.
    When the user makes the "POST" request to the endpoint.
    Then the request fails with the status code "500".
    And the customer account is not registered.
