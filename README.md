# Parade Bulk Event Uploader

Simple Python 3 script used to batch upload events to [Parade](https://parade.events/) given a delimited file.

Parade backend is running GraphQL with auth sent via the Authorization header.

## Setup

Utilizes prisma's [python-graphql-client](https://github.com/prisma/python-graphql-client) to wrap the GraphQL requests.  

Install by running `pip install graphqlclient`

## Usage

First, set environment variable `PARADE_JWT` to a valid Parade token.  

Next, edit the `ENDPOINT` and `ORGANIZATION_ID` variables accordingly.

Now execute:

`python3 main.py <INPUT FILE>`

## Input
Read in a CSV file with THIS header, and each column aligned with the following (note the trailing `|`):
`title|description|startTime|endTime|location|imageUrl|`

Each field is delimited by a pipe (`|`).

See the [example file](./example.pipe).


## Tips
A useful excel formula to get times formatted properly. Note the +4 to account for Boston time.

`=CONCATENATE(filtered!A1,"T",TEXT((filtered!C1 + TIME(4,0,0)), "hh:mm:ss"), "Z")`

