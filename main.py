# Parade Bulk Event Uploader
# Josh Spicer <josh@parade.events>
# Hits our GraphQL endpoint, uploading contents of given CSV.

from graphqlclient import GraphQLClient
import os
import sys

## VARIABLES ##
ENDPOINT = ''
ORGANIZATION_ID = ''

if ENDPOINT == '' or ORGANIZATION_ID == '':
    print('[-] Must set ENDPOINT and ORGANIZATION_ID variables')
    exit(1)

# Set a valid Parade token as an environment variable for auth.
try:
    token = os.environ['PARADE_JWT']
except:
    print("[-] Must set environment variable: PARADE_JWT")
    exit(1)

if len(sys.argv) != 2:
    print("[-] Supply a properly formatted .csv file as the first argument.")
    exit(1)


# Validates the event input, and submits if good.
def handleLine(line, idx):
    try:
        ss = line.split('|')
        if len(ss) != 7:
            print("[-] Invalid line length on event index {}".format(idx))
            return

        evt = {
            "event": {},
            "description": {}
        }

        evt['event']['organizationId'] = ORGANIZATION_ID

        # Required Fields
        evt['event']['title'] = ss[0]
        evt['event']['startTime'] = ss[2]
        evt['event']['location'] = ss[4]

        # Optional
        if ss[3] != '':
            evt['event']['endTime'] = ss[3]
        if ss[1] != '':
            evt['description']['full'] = ss[1]
        if ss[5] != '':
            evt['event']['imageUrl'] = ss[5]

        submit(evt)

    except Exception as err:
        print("[-] Error on event index {}. Error: {}".format(idx, err))


# Parses input file, calling handleLine() on each line.
def parseFile():
    with open(sys.argv[1]) as f:
        # Skip over the first line of the file,
        # as that should be the header
        header = f.readline()
        # Enumerate each line
        for idx, line in enumerate(f):
            handleLine(line, idx)


# Submit an event
def submit(evt):
    client = GraphQLClient(ENDPOINT)
    client.inject_token('Bearer {0}'.format(token))

    # Execute createEvent mutation
    result = client.execute('''
    mutation createEvent($event: EventInput!, $description: DescriptionInput!) {
        createEvent(event: $event, description: $description) {
            id
            }
        } 
        ''', variables={"event": evt['event'], "description": evt['description']})

    # Print result (error, or new event ID)
    print(result)


# Kick off program
def init():
    parseFile()


if __name__ == "__main__":
    init()
