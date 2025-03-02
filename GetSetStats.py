import DataHelper


# STATUS: FINISHED
# getting specific stats for the user
async def get_stat(user_id, stat):
    users = await DataHelper.get_player_data()
    return users[str(user_id)][stat]


# increase the total points by one
async def increase_points(user_id, points_type):
    users = await DataHelper.get_player_data()
    users[str(user_id)][points_type] += 1
    await DataHelper.update_player_data(users)


# add this player to the author's already visited list
async def update_already_visited(visitor_id, visited_id):
    users = await DataHelper.get_player_data()
    users[str(visitor_id)]["List Of Visitors"].append(visited_id)
    await DataHelper.update_player_data(users)


# decrease trashability by one
async def decrease_trashability(user_id):
    users = await DataHelper.get_player_data()
    users[str(user_id)]["Trashability"] -= 1
    await DataHelper.update_player_data(users)


# update status
async def update_status(user_id, new_status, status_type):
    users = await DataHelper.get_player_data()
    users[str(user_id)][status_type] = new_status
    await DataHelper.update_player_data(users)


# host command updates
async def update_giving_gift_stats(author_id, player_id, gift_type):
    await update_status(player_id, gift_type, "Received")
    await update_status(player_id, author_id, "Giver")
    await update_status(author_id, False, "Visited")
    await update_status(player_id, False, "Visiting")


# visiting command updates
async def update_successful_visit_stats(author_id, player_id):
    await update_status(author_id, player_id, "Visiting")
    await update_status(player_id, author_id, "Visited")


async def update_successful_home_stats(author_id, player_id):
    await update_status(author_id, False, "Visiting")
    await update_status(player_id, False, "Visited")


# guest command updates
async def update_unbox_nice_stats(author_id, giver_id):
    await increase_points(author_id, "Total Points")
    await increase_points(author_id, "Unboxed Points")
    await increase_points(author_id, "Trashability")

    await update_status(author_id, False, "Received")
    await update_status(author_id, False, "Giver")
    await update_status(author_id, True, "Join")
    await update_status(giver_id, True, "Join")

    await update_already_visited(author_id, giver_id)


async def update_unbox_devious_stats(author_id, giver_id):
    await increase_points(giver_id, "Total Points")
    await increase_points(giver_id, "Kill Points")

    await update_status(author_id, False, "Received")
    await update_status(author_id, False, "Giver")
    await update_status(author_id, True, "Join")
    await update_status(giver_id, True, "Join")

    await update_status(author_id, True, "Dead")
    await update_already_visited(author_id, giver_id)


async def update_decline_nice_stats(author_id, giver_id):
    await increase_points(giver_id, "Total Points")
    await increase_points(giver_id, "Declined Points")

    await update_status(author_id, False, "Received")
    await update_status(author_id, False, "Giver")
    await update_status(author_id, True, "Join")
    await update_status(giver_id, True, "Join")
    await update_already_visited(author_id, giver_id)


async def update_decline_devious_stats(author_id, giver_id):
    await increase_points(author_id, "Total Points")
    await increase_points(author_id, "Accidental Kill")

    await update_status(author_id, False, "Received")
    await update_status(author_id, False, "Giver")
    await update_status(author_id, True, "Join")
    await update_status(giver_id, True, "Join")

    await update_status(giver_id, True, "Dead")
    await update_already_visited(author_id, giver_id)


async def update_trashing_stats(author_id, giver_id):
    await decrease_trashability(author_id)

    await update_status(author_id, False, "Received")
    await update_status(author_id, False, "Giver")
    await update_already_visited(author_id, giver_id)
