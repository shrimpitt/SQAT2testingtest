Feature: Flight Search on Aviasales
  As a user
  I want to search for flights
  So that I can find available options

  Scenario: Search for available flights
    Given I am on the Aviasales homepage
    When I disable the Booking.com checkbox
    And I enter "Астана" as departure city
    And I enter "Уральск" as destination city
    And I select departure date "28.02.2025"
    And I click the search button
    Then I should see available flight options
