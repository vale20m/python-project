import python_project

def test_validate_username_re():
    account = python_project.Account("123", "")
    assert python_project.validate_username_re(account) == None
    account.username = "Valentin1"
    assert python_project.validate_username_re(account) != None
    account.username = "ThisIsAVeryLongName"
    assert python_project.validate_username_re(account) == None
    account.username = "RonnieJames_Dio"
    assert python_project.validate_username_re(account) != None

def test_validate_password_re():
    account = python_project.Account("", "")
    assert python_project.validate_password_re(account) == None
    account.password = "12345"
    assert python_project.validate_password_re(account) == None
    account.password = "password"
    assert python_project.validate_password_re(account) != None
    account.password = "VeryLongPassword123!?"
    assert python_project.validate_password_re(account) != None

def test_validate_topic_name():
    assert python_project.validate_topic_name("ShortName") == None
    assert python_project.validate_topic_name("This is a correct name!!") != None
    assert python_project.validate_topic_name("This name is too long to be correct for the program") == None
    assert python_project.validate_topic_name("TOTALLY VALID TOPIC_NAME") != None

def test_validate_comment():
    assert python_project.validate_comment("") == None
    assert python_project.validate_comment("This is a completely normal comment") != None
    assert python_project.validate_comment("This comment is not valid: 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000") == None
    assert python_project.validate_comment(":D") != None