"""
Copyright 2019 Kaeo-19, Nasanian


Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import json
import datetime

#Global variables
dtn = datetime.datetime.now()


#TESTING: PASSED
def create_profile( member_id: int = None, member_name: str = " ", rank: str = "N/a", dm_status: str = "Closed", gender: str = "N/a", bio: str = "", profile_creation_date: str = str("{}\{}\{}\{}\{}\{}".format(dtn.year, dtn.month, dtn.day, dtn.hour, dtn.minute, dtn.second))) -> str:
    """Writes the profile information to a json file"""
    with open("./users/" + str(member_id) + ".json", "w") as user_file:
        file_format = {
            "{}".format(str(member_id)): {
                "name": member_name,
                "profile_created_at": profile_creation_date,
                "rank": str(rank),
                "dm_status": dm_status,
                "gender": gender,
                "bio": bio,
                "bio_id": str(member_id),
                "wallet": 0
            }
        }

            
            
        
        json_obj = json.dumps(file_format, indent=4)
        user_file.write(json_obj)
        user_file.close()
        return "User filecreated for {} at {}".format(member_id, profile_creation_date)

def delete_profile(member_id: str = None) -> str:
    """Deletes a users profile. Run this when the user leaves the server so we don't have useless json files."""
    os.remove("../users/{}.json".format(member_id))
    return "Profile Deleted."
        

def edit_profile(member_id: str = None, element: str = None, value: str = None) -> str:
    """Change a user profiles entry"""
    
    with open('../users/{}.json'.format(member_id), "rw") as user_file:
        
        user_file = json.loads(user_file)
        user_file[member_id][element] = value
        user_file.close()
        return "Element {} changed to {}".format(element, value)
    
def view(member_id: str = None) -> list:
    """View a user profile"""
    if member_id is None:
        return "User id cannot be none!"
    else:
        with open('./users/{}.json'.format(member_id), "r") as member_file:
            member_data = json.load(member_file)
            #Return a json dictionary so that it can be parsed as neccesary in the main file
            return member_data

def list_profiles() -> list:
    
    profiles = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        profiles.extend(filenames)

    #Return a list
    return profiles









                                      
