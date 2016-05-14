from app.models.post import PostModel
from app.models.tag import TagModel
from app.models.comment import CommentModel
from app.common.utils import random_number, slugify, id_generator


Tags = ['Computer Science', 'Dynamic Programming', 'Djikstrs',
        'Sorting', 'Median', 'Two Sum', 'Hard', 'Easy', 'Medium',
        'Matrix', 'Differential', 'Recursion', 'Lazy', 'Partial',
        'Parallel', 'Design Pattern']

def create_posts():
    """ generate random posts """
    for i in range(150):
        tag = [ Tags[random_number(0,len(Tags)-1)], Tags[random_number(0,len(Tags)-1)] ]
        post = " ".join(map(''.join, zip(*[iter(id_generator(500))]*random_number())))
        description = " ".join(map(''.join, zip(*[iter(id_generator(100))]*random_number())))
        title = " ".join(map(''.join, zip(*[iter(id_generator(25))]*random_number())))
        slugid = slugify(title) # check if this already exists - if so, throw or pass
        pm = PostModel( Title = title, Post=post, Tags=tag, Description=description, Published=True, id=slugid )
        pm.put()
        postId = pm.key.id()
        for tg in tag:
            TagModel.create_or_update_tag(tg)
        for i in xrange(random_number(3,15)):
            comment = " ".join(map(''.join, zip(*[iter(id_generator(100))]*random_number())))
            username = id_generator(random_number(6,15))
            email = ".".join([ "@".join([username, id_generator(random_number(5,10))]), "com" ])
            cm = CommentModel( Name=username, Email=email, Comment=comment, SlugId=slugid, Published=True )
            cm.put()
