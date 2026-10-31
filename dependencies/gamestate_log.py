gamestage_mainChapters = [
    '0', '1', '2'
]
next_subchapter_key = {
    '0-0001': '0-0002'
}

gamestage_subchapters = {
        '0' : {'0001': {'name': 'The Inn',
                        'reqs': ['puzzle0001', 'speak0002'],
                        'desc': 'I think its time for bed, best do my list or else madam will be mad',
                        'actions': ['speak_0001', 'puzzle_0001', 'speak_0002'],
                        'imagepath': 'innBedroom.jpeg'
                        },
             '0002': {'name': 'Streets',
                      'reqs': ['dialogue_0002']
                      },
             '0003': {'name': 'Doctors Office',
                      'reqs': ['dialogue_0003', 'dialogue_0004']}
            }
}
