import database.loadhost as lh
cursor_types = {
    'reader': {
        "host":lh.global_host,
        "user": lh.reader_user,
        "password": lh.reader_password,
        "database": lh.db_name
    },
    'writer': {
        "host":lh.global_host,
        "user": lh.writer_user,
        "password": lh.writer_password,
        "database": lh.db_name 
    }
}
