import aiohttp
import asyncio
import requests
import textwrap
import html2text


def get_top_stories(limit=40):
    """
    Prints the X top stories of hacker news when x equals to the given limit (default value = 40) ordered by their rank.
    print format: <rank>. <story title> : <story url>.
    """
    if limit is None or limit < 1:
        limit = 40

    # Get the top stories ids
    stories_ids = get_top_stories_ids(limit)

    # Get the stories data by their ids
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_stories_data(stories_ids))


def get_top_stories_ids(limit):
    """
    returns a list with the X top stories-ids of hacker news when x equals to the given limit
    """
    get_stories_id_url = \
        'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty&limitToFirst={}&orderBy="$key"' \
            .format(limit)

    try:
        results = requests.get(get_stories_id_url).json()
    except Exception as e:
        raise type(e)(str(e) + ' happens at get_top_stories_ids')
    return results


async def get_stories_data(stories_ids):
    """
    Prints the given stories data.
    :param stories_ids: A list of stories ids ordered by their rank.
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for (i, story_id) in enumerate(stories_ids):
            task = asyncio.ensure_future(get_story_data(session, story_id, i+1))
            tasks.append(task)

        stories_data = await asyncio.gather(*tasks)
        stories_data.sort(key=lambda x:x[0])

    print("The top stories in Hacker News:\n")
    [print("{}. {} : {} \n".format(story[0], story[1], story[2])) for story in stories_data]


async def get_story_data(session, story_id, story_rank):
    """
    Gets the given story data - title and url
    """
    url = 'https://hacker-news.firebaseio.com/v0/item/{}.json'.format(story_id)

    async with session.get(url) as response:
        result_data = await response.json()

        story_url = ""
        if "url" in result_data:  # The url key might not be in the results data
            story_url = result_data['url']

        return story_rank, result_data['title'], story_url


def get_comments_by_story_rank(rank):
    stories_ids = get_top_stories_ids(rank)

    story_id = stories_ids[rank-1]

    story_data_url = 'http://hn.algolia.com/api/v1/items/{}'.format(story_id)

    try:
        story_data = requests.get(story_data_url).json()
    except Exception as e:
        raise type(e)(str(e) + ' happens when trying to get story data')

    # check if we have comments on this story
    if 'children' in story_data and len(story_data['children']) > 0:
        print_comments(story_data['children'])


def print_comments(comments, indent_num=0):
    """
    Prints the given comments thread recursively while preserving the comment indentation level
    """
    for comment in comments:  # iterate over comments
        comment_txt = ""
        if 'text' in comment and comment["text"] is not None:
            comment_txt = comment["text"]

        author_name = ""
        if 'author' in comment and comment["author"] is not None:
            author_name = comment["author"]

        print_comment(author_name, comment_txt, indent_num)

        if 'children' in comment and len(comment['children']) > 0:
            print_comments(comment['children'], indent_num+1)  # print replies using the same function


def print_comment(author_name, comment_txt, indent_num):
    """
    Prints the given comment data indented according to the given indent number.
    Comment print format - <author_name> : <comment_txt>
    """
    if author_name == "" and comment_txt == "":
        return

    text = str(author_name + " : " + html2text.html2text(comment_txt))
    my_warp = textwrap.TextWrapper()
    comment_list = my_warp.wrap(text=text)
    for line in comment_list:
        print("\t" * indent_num + line)

    print("\n")  # add another \n to separate between the comments

