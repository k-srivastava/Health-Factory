# Health Factory

## Abstract

The objective with this project is to create a one-stop solution for a local pharmacy to be able to manage and maintain
their database of employee and product data without having to create one themselves and without the overhead of a
technical team or licensing from a commercial vendor.

The project uses robust technologies like `SQLite` and `Python` for the back-end and `Flask` as the middle-ware allowing
for the project to be reasonably scaled up to meet all the requirements a local pharmacy could want.

## Table of Contents

1. [Design](#design)
2. [Implementation](#implementation)
3. [Testing](#testing)
4. [Result Analysis](#result-analysis)
5. [Conclusion](#conclusion)

## Design

The project uses `Python` for the backend and `SQLite` as the database. `Python` has a package called `Flask` that acts
as the middle-end for the project. It ensures connection between the frontend and the backend and allows for more
complex functions like page routing and form submission using `GET` and `POST` HTTP methods.

The project is organised into various modules that handle common functionality like frontend dependency management,
backend database connection and more. To interact with the database, a custom lite-ORM has been written from scratch
that models the database relations in `Python` using `dataclasses`. The project is also extensively tested especially
for database interactions, which includes a smaller test database.

It is hosted in GitHub and uses open-source software wherever possible and can be forked and modified as required by the
customer if required.

## Implementation

## Testing

## Result Analysis

## Conclusion
