*****************************************************
*                                                   *
*   Technical Test for Java/Web Developer Position  *
*   Robert Williams                                 *
*   28/04/2017                                      *
*                                                   *
*****************************************************

This approach uses Flask in order to provide the RESTful API endpoints.

As noted in the source code, there are some discrepancies between the
ordering defined in the requirement specification due to the way in
which Flask serialises the response data, so apologies if the explicit
ordering was a hard requirement, you will find that all of the data is,
however, present :)

#########
# USAGE #
#########

The .exe can be executed directly, and will assume that there will be a
data file matching the format of the one provided present in the same
location named "games_data.json".
It can also be run from the commandline with an alternative filename
provided as its single argument (or the source file dragged and dropped
onto the executable.

The source script can be run directly from the commandline as well, but
has the dependency on Flask being present.
The script functions identically to the .exe in regards to the source
data location (although sadly not the drag and drop).