Feature: Account registry

Scenario: User is able to create 2 accounts
    Given Account registry is empty
    When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    And I create an account using name: "tadeusz", last name: "szcześniak", pesel: "79101011234"
    Then Number of accounts in registry equals: "2"
    And Account with pesel "89092909246" exists in registry
    And Account with pesel "79101011234" exists in registry

Scenario: User is able to update surname of already created account
    Given Acoount registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    When I update "surname" of account with pesel: "95092909876" to "filatov"
    Then Account with pesel "95092909876" has "surname" equal to "filatov"

Scenario: User is able to update name of already created account
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    When I update "name" of account with pesel: "95092909876" to "nataliia"
    Then Account with pesel "95092909876" has "name" equal to "nataliia"

Scenario: Created account has all fields correctly set
    Given Account registry is empty
    When I create an account using name: "jan", last name: "kowalski", pesel: "12345678901"
    Then Account with pesel "12345678901" has "name" equal to "jan"
    And Account with pesel "12345678901" has "surname" equal to "kowalski"
    And Account with pesel "12345678901" has "pesel" equal to "12345678901"
    And Account with pesel "12345678901" has "balance" equal to "0"

Scenario: User is able to delete created account
    Given Account registry is empty
    And I create an account using name: "parov", last name: "stelar", pesel: "01092909876"     
    When I delete account with pesel: "01092909876"
    Then Account with pesel "01092909876" does not exist in registry
    And Number of accounts in registry equals: "0"

Scenario: User is able to make incoming transfer
    Given Account registry is empty
    And I create an account using name: "test", last name: "user", pesel: "11111111111"
    When I make an incoming transfer of "100.0" to account with pesel "11111111111"
    Then Account with pesel "11111111111" has balance equal to "100.0"

Scenario: User is able to make outgoing transfer
    Given Account registry is empty
    And I create an account using name: "test", last name: "user", pesel: "22222222222"
    And I make an incoming transfer of "100.0" to account with pesel "22222222222"
    When I make an outgoing transfer of "50.0" from account with pesel "22222222222"
    Then Account with pesel "22222222222" has balance equal to "50.0"

Scenario: Outgoing transfer fails when funds are insufficient
    Given Account registry is empty
    And I create an account using name: "test", last name: "user", pesel: "33333333333"
    And I make an incoming transfer of "10.0" to account with pesel "33333333333"
    When I make an outgoing transfer of "50.0" from account with pesel "33333333333"
    Then Transfer fails with status code "422"
    And Account with pesel "33333333333" has balance equal to "10.0"