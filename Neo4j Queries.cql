Neo4j Queries

Get the top 5 handles by # of followers
MATCH (u:User)WHERE u.followers > 0 RETURN u.screen_name, u.followers ORDER BY u.followers DESC LIMIT (5)

Get tweets and user handles of tweets containing "fraud" and "bernie"

MATCH (u:User)-[:POSTS]->(t:Tweet) WHERE t.text CONTAINS "Fraud" AND t.text CONTAINS "Bernie" RETURN t.text as Tweet, u.screen_name as User

Get the number of distnct twitter users posting tweets

MATCH (u:User)-[r:POSTS]->(t:Tweet) RETURN count(DISTINCT u) as Distinct_Users

Get the number of distinct tweets collected in our DB

MATCH (u:User)-[r:POSTS]->(t:Tweet) RETURN count(DISTINCT t)

Get max# retweets

MATCH (retweet:Tweet)-[rt:RETWEETS]->(orig:Tweet)<-[:POSTS]-(u:User) RETURN u.screen_name as User, COUNT(rt) as Retweets ORDER BY COUNT(rt) DESC LIMIT 5

get retweets relationship graph thing

MATCH rts=(retweet:Tweet)-[rt:RETWEETS]->(orig:Tweet)<-[:POSTS]-(u:User) RETURN rts

get the top 10 screen names with the most mentions

MATCH ment=(t:Tweet)-[mention:MENTIONS]->(u:User) RETURN u.screen_name, COUNT(u.screen_name)as NUM_Mentions ORDER BY NUM_Mentions DESC Limit (10)

follow metric

MATCH (u:User) WHERE u.followers > 0 RETURN u.screen_name, toFloat( u.followers)/ 962450 * 100 ORDER BY toFloat( u.followers)/ 962450 DESC

Set each user's follow_metric based on their proportion of followers compared to the max in the set.

MATCH (u:User) WHERE u.followers > 0 SET u.follow_metric = toFloat( u.followers)/ 962450 * 100 RETURN u.screen_name, toFloat( u.followers)/ 962450 * 100 ORDER BY toFloat( u.followers)/ 962450 DESC

Set each user's retweet_count to 0

MATCH (u:User) SET u.retweet_count = 0

Increment user's retweet_count for each retweet found

MATCH (retweet:Tweet)-[rt:RETWEETS]->(orig:Tweet)<-[:POSTS]-(u:User) SET u.retweet_count = u.retweet_count+1  RETURN u.screen_name as User, COUNT(rt) as Retweets ORDER BY COUNT(rt) DESC

Set each users's retweet score based on their proportion of retweets compared to the max in the set

MATCH (u:User) where u.retweet_count > 0 SET u.retweet_score = toFloat(u.retweet_count)/123095 *100

Get user with the highest average sentiment toward bernie sanders

MATCH (u:User)-[:POSTS]->(t:Tweet) WHERE t.text CONTAINS "Bernie" RETURN u.screen_name, COUNT(u.screen_name), avg(t.sentimentScore) ORDER BY avg(t.sentimentScore) DESC

Get max # following

MATCH (u:User) RETURN max(u.following)

Set each user's following_score based on their proportion of following compared to max in the set

MATCH (u:User) where u.following > 0 SET u.following_score = toFloat(u.following)/450389 *10

Set each user's favorite count to o

MATCH (u:User) SET u.fav_count = 0

Add each tweet's favorite count to the appropriate user

MATCH (u:User)-[:POSTS]->(t:Tweet) SET u.fav_count = u.fav_count + t.favorites

Get max fav_count

MATCH (u:User) RETURN max(u.fav_count)

Set all users' fav_score to 0

MATCH (u:User) SET u.fav_score = 0

Set each user's fav_score based on their proportion of favorites compared to the max

MATCH (u:User) SET u.fav_score = toFloat(u.fav_count) / 108256 * 10

Set each user's influence score

MATCH (u:User) SET u.InfluenceScore = u.follow_metric + u.retweet_score + u.fav_score + u.following_score

