# eve_nav
Django API for basic EVE navigational utilities

URLS:
 - Finding the number of jumps and fastest route between two systems using their IDs:
 
`/api/v1/route/<Origin ID>/<Destination ID>/`

 - Finding the number of jumps and fastest route between two systems using their names:
 
`/api/v1/route/<Origin Name>/<Destination Name>/`

 - Finding the light year difference between two systems using their IDs:

`/api/v1/route/<System1 ID>/<System2 ID>/`

 - Finding the light year difference between two systems using their names:

`/api/v1/route/<System1 Name>/<System2 Name>/`

 - Finding all system IDs within jump range of a specified System ID and a specified jump range:

`/api/v1/jumps/<System ID>/<Jump Range>/`

 - Same as above, but finding multiple systems with multiple jump ranges:

`/api/v1/jumps/<System ID #1>, <System ID #2>, <System ID #3>/<Jump Range #1>, <Jump Range #2>, <Jump Range #3>/`

