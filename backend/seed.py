from app import create_app, db
from app.models import Passage

app = create_app()

with app.app_context():
    Passage.query.delete()
    db.session.commit()

    text1 = "The mechanics were working on one out in the yard. Three others were up in the mountains at dressing stations."
    passage1 = Passage(
        text = text1,
        title = 'A farewell to arms',
        author = 'Ernest Hemingway',
        length = len(text1.split()),
        difficulty = 'beginner'
    )

    text2 = "Well, it was no use mincing the matter, I told her all. She listened with awe, and for some minutes she could not speak."
    passage2 = Passage(
        text = text2,
        title = 'A Journey to the Centre of the Earth',
        author = 'Jules Verne',
        length = len(text2.split()),
        difficulty = 'beginner'
    )

    text3 = "The red light burns steadily all the evening in the lighthouse on the margin of the tide of busy life."
    passage3 = Passage(
        text = text3,
        title = 'The Mystery of Edwin Drood',
        author = 'Charles Dickens',
        length = len(text3.split()),
        difficulty = 'beginner'
    )

    text4 = "As we passed across the lawn on our way to the station to catch our train we could see the front of the asylum. I looked eagerly, and in the window of my room saw Mina. I waved my hand to her, and nodded to tell that our work there was successfully accomplished. She nodded in reply to show that she understood. The last I saw, she was waving her hand in farewell. It was with a heavy heart that we sought the station and just caught the train, which was steaming in as we reached the platform."
    passage4 = Passage(
        text = text4,
        title = 'Dracula',
        author = 'Bram Stoker',
        length = len(text4.split()),
        difficulty = 'intermediate'
    )

    text5 = "The players all played at once without waiting for turns, quarrelling all the while, and fighting for the hedgehogs; and in a very short time the Queen was in a furious passion, and went stamping about, and shouting “Off with his head!” or “Off with her head!” about once in a minute."
    passage5 = Passage(
        text = text5,
        title = "Alice's Adventures in Wonderland",
        author = 'Lewis Carroll',
        length = len(text5.split()),
        difficulty = 'intermediate'
    )

    text6 = "Poor Marilla was only preserved from complete collapse by remembering that it was not irreverence, but simply spiritual ignorance on the part of Anne that was responsible for this extraordinary petition. She tucked the child up in bed, mentally vowing that she should be taught a prayer the very next day, and was leaving the room with the light when Anne called her back."
    passage6 = Passage(
        text = text6,
        title = 'Anne of Green Gables',
        author = 'L.M. Montgomery',
        length = len(text6.split()),
        difficulty = 'intermediate'
    )

    text7 = "Had she found Jane in any apparent danger, Mrs. Bennet would have been very miserable; but being satisfied on seeing her that her illness was not alarming, she had no wish of her recovering immediately, as her restoration to health would probably remove her from Netherfield. She would not listen therefore to her daughter's proposal of being carried home; neither did the apothecary, who arrived about the same time, think it at all advisable. After sitting a little while with Jane, on Miss Bingley's appearance and invitation, the mother and three daughters all attended her into the breakfast parlour. Bingley met them with hopes that Mrs. Bennet had not found Miss Bennet worse than she expected."
    passage7 = Passage(
        text = text7,
        title = 'Pride and Prejudice',
        author = 'Jane Austen',
        length = len(text7.split()),
        difficulty = 'advanced '
    )

    text8 = "By and by they passed the mouth of the Ohio; they passed cane-brakes; they fought mosquitoes; they floated along, day after day, through the deep silence and loneliness of the river, drowsing in the scant shade of makeshift awnings, and broiling with the heat; they encountered and exchanged civilities with another party of Indians; and at last they reached the mouth of the Arkansas (about a month out from their starting-point), where a tribe of war-whooping savages swarmed out to meet and murder them; but they appealed to the Virgin for help; so in place of a fight there was a feast, and plenty of pleasant palaver and fol-de-rol."
    passage8 = Passage(
        text = text8,
        title = 'Life on the Mississippi',
        author = 'Mark Twain',
        length = len(text8.split()),
        difficulty = 'advanced'
    )

    text9 = "While he was speaking Zaidie had taken off a Spanish mantilla which she had thrown over her head as she came out, and which the ladies of Venus seemed to think was part of her hair. Then she took out the comb and one or two hairpins which kept the coils in position, deftly caught the ends, and then, after a few rapid movements of her fingers, she shook her head, and the wondering crowd about her saw, what seemed to them a shimmering veil, half gold, half silver, in the soft reflected light from the cloud-veil, fall down from her head over her shoulders."
    passage9 = Passage(
        text = text9,
        title = 'A Honeymoon in Space',
        author = 'George Chetwynd Griffith',
        length = len(text9.split()),
        difficulty = 'advanced'
    )

    db.session.add(passage1)
    db.session.add(passage2)
    db.session.add(passage3)
    db.session.add(passage4)
    db.session.add(passage5)
    db.session.add(passage6)
    db.session.add(passage7)
    db.session.add(passage8)
    db.session.add(passage9)
    db.session.commit()