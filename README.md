## API

### BaseMethodsAPI
### 1. sendCode
  + **Отправляет код на почту**
  + **Параметры:**
    + **email** - почта куда отправить
  + **Ответы:**
    ```
    {
        "ok" : true
    }
    ```
  + **Ошибки:**
    + Invalid email

### 2. signIn
  + **Авторизация**
  + **Параметры:**
    + **email** - почта
    + **code** - код отправленный на почту (шестизначное число)
  + **Ответы:**
    ```
    {
        "ok" : true,
        "is_auth" : true,
        "description" : 'You are logged in',
        "token" : "Rj6pfPSCIKYDnqlLeO2EA7GxthFQ3bHg"
    }
    ```
    ```
    {
        "ok" : true,
        "is_auth" : false,
        "description" : "Register now",
        "token" : "Rj6pfPSCIKYDnqlLeO2EA7GxthFQ3bHg"
    }
    ```
  + **Ошибки:**
    + No login required
    + The waiting time has expired
    + Incorrect code

### 3. register
  + **Регистрация в аккаунт**
  + **Параметры:**
    + **token** - токен сессии (32 символа)
    + **code** - код отправленный на почту (шестизначное число)
    + **name** - имя (16 символов)
    + **surname (опционально)** - фамилия (16 символов)
    + **description (опционально)** - описание (64 символов)
  + **Ответы:**
    ```
    {
        "ok" : true,
        "description" : "Are you registered"
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + You are already registered
    + The waiting time has expired
    + Invalid parameters

### 4. logOut
  + **Выход из аккаунта**
  + **Параметры:**
    + **token** - токен сессии (32 символа)
  + **Ответы:**
    ```
    {
        "ok" : true
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found

## ProfileMethodsAPI

### 1. me
  + **Информация об аккаунте**
  + **Параметры:**
    + **token** - токен сессии (32 символа)
  + **Ответы:**
    ```
    {
        "ok": true,
        "result": {
            "_id": 1,
            "contacts": [],
            "description": null,
            "email": "ku6ikru6ika@gmail.com",
            "groups": [],
            "name": "Кубик",
            "surname": null
        }
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found

## GroupsMethodsAPI

### 1. createGroup
  + **Создать группу**
  + **Параметры:**
    + **token** - токен сессии (32 символа)
    + **name** - название группы
    + **link (опционально)** - ссылка на группу
    + **description (опционально)** - описание группы
  + **Ответы:**
    ```
    {
        "ok": true,
        "result": {
            "_id": 1,
            "description": null,
            "link": null,
            "messages": [],
            "name": "Чат",
            "owner": 1,
            "participants": [
              1
            ]
        }
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + Invalid parameters

### 2. joinGroup
  + **Войти в группу**
  + **Параметры:**
    + **token** - токен сессии (32 символа)
    + **id_group** - айди группы
  + **Ответы:**
    ```
    {
        "ok": true,
        "result": {
            "_id": 1,
            "description": null,
            "link": null,
            "messages": [],
            "name": "Чат",
            "owner": 1,
            "participants": [
              1, 2
            ]
        }
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + Invalid group id
    + Group not found
    + You are already in a group

### MessagesMethodsAPI

### 1. sendMessage
  + **Отправить сообщение в группу**
  + **Параметры:**
    + **token** - токен сессии (32 символа)
    + **id_group** - айди группы
    + **text** - текст сообщение (2048 символов)
  + **Ответы:**
    ```
    {
        "ok": true,
        "result": {
            "_id": 1,
            "date": "Wed, 03 Nov 2021 17:23:50 GMT",
            "from_id": 1,
            "text": "Привет"
        }
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + Group not found
    + You are not in this group
    + Invalid parameters

### 2. getMessages
  + **Получить список сообщений группы**
  + **Параметры:**
    + **token** - токен сессии (32 символа)
    + **id_group** - айди группы
  + **Ответы:**
    ```
    {
        "ok": true,
        "result": [
            {
                "_id": 1,
                "date": "Wed, 03 Nov 2021 17:23:50 GMT",
                "from_id": 1,
                "text": "Привет"
            }
        ]
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + Group not found
    + You are not in this group