@api
Feature: 002 Login Customer Account on Parabank

  Scenario: 2.1 - An unregistered user can not login into customer account on Parabank without valid credentials.
    Given the user has already visited the homepage of parabank.
    And the user has a public endpoint to login into the customer account.
    And the user has "invalid" credentials to login into the customer account.
    When the user makes the "POST" request to the endpoint.
    Then the request passes with the status code "200".
    And the user can see the message "The username and password could not be verified.".

  @create_account
  Scenario: 2.2 - A registered user can login into customer account on Parabank with valid credentials.
    Given the user has a public endpoint to login into the customer account.
    And the user has "valid" credentials to login into the customer account.
    When the user makes the "POST" request to the endpoint.
    Then the request passes with the status code "302".

  @create_account
  Scenario: 2.3 - A registered user can access dashboard overview screen after successful login into customer account.
    Given the user has already logged into the customer account using valid credentials.
    And the user has a private endpoint to visit the dashboard overview of parabank.
    When the user makes the "GET" request to the endpoint.
    Then the request passes with the status code "200".
    And the user can see the message "Accounts Overview".

  @create_account
  Scenario: 2.4 - A logged in user can log out of parabank account.
    Given the user has already logged into the customer account using valid credentials.
    And the user has a private endpoint to logout of the customer account of parabank.
    When the user makes the "GET" request to the endpoint.
    Then the request passes with the status code "302".
    And the user is logged out of the customer account of parabank.
