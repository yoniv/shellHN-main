import click
import hn_api
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')

file_handler = logging.FileHandler('logs/shell_hn.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


@click.group()
def shell():
    """
    Simple CLI for hacker news
    """
    pass


@shell.command()
def top():
    """Returns the top 40 stories in HN ordered by their rank (1..40)"""
    logger.info("Getting top stories.")
    try:
        hn_api.get_top_stories()
    except Exception as e:
        err_msg = "Getting top stories failed with error: {}".format(e)
        logger.error(err_msg)
        print(err_msg)


@shell.command()
def comments():
    """Returns the comments thread of the story who has the given rank"""
    rank = click.prompt("Please enter the story's rank", type=int)
    while rank <= 0 or rank > 500:
        if rank <= 0:
            rank = click.prompt("The rank must be positive, please try again", type=int)
        if rank > 500:
            rank = click.prompt("The maximum rank is 500, please try again", type=int)

    logger.info("Getting story #{} commands.".format(rank))
    try:
        hn_api.get_comments_by_story_rank(rank)
    except Exception as e:
        err_msg = "Getting story #{} commands failed with error: {}".format(rank, e)
        logger.error(err_msg)
        print(err_msg)
