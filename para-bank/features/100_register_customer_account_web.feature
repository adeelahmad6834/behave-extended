@web
Feature: 100 Register Customer Account.

  Scenario: 100.1 - a new user can access the registration page from Parabank Homepage.
    Given the user is on the home page of Parabank.
    When the user clicks on the "Register" button.
    Then the user is redirected to "Registration" page.
    And the user can see a message "Signing up is easy!".

  Scenario: 100.2 - a new user can create a customer account by providing required details.
    Given the user is already on the registration page of Parabank.
    When the user enters "fname" in the "First Name" field.
    And the user enters "lname" in the "Last Name" field.
    And the user enters "addr" in the "Address" field.
    And the user enters "city" in the "City" field.
    And the user enters "state" in the "State" field.
    And the user enters "zip code" in the "Zip Code" field.
    And the user enters "1122" in the "SSN" field.
    And the user enters "admin" in the "Username" field.
    And the user enters "Test@123" in the "Password" field.
    And the user enters "Test@123" in the "Confirm" field.
    And the user submits the form by clicking on the Register button.
    Then the user is redirected to "Dashboard" page.
    And the user can see a message "Welcome".
