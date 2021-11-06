## API

### Последние изменения
  + **Добавлены личные сообщения**
  + **Добавлены новые методы настройки**
  + **Обновленны старые методы**

### BaseMethodsAPI
### 1. sendCode - POST
  + **Отправляет код на почту**
  + **Параметры - application/json**
    + **email** - почта куда отправить
  + **Ответы:**
    ```json
    {
        "ok" : true
    }
    ```
  + **Ошибки:**
    + Invalid email

### 2. signIn - POST
  + **Авторизация**
  + **Параметры - application/json**
    + **email** - почта
    + **code** - код отправленный на почту (шестизначное число)
  + **Ответы:**
    ```json
    {
        "ok" : true,
        "is_auth" : true,
        "description" : "You are logged in",
        "token" : "Rj6pfPSCIKYDnqlLeO2EA7GxthFQ3bHg"
    }
    ```
    ```json
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
    + Invalid parameters

### 3. register - POST
  + **Регистрация в аккаунт**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **name** - имя (16 символов)
    + **surname (опционально)** - фамилия (16 символов)
    + **description (опционально)** - описание (64 символов)
  + **Ответы:**
    ```json
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

### 4. logOut - POST
  + **Выход из аккаунта**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
  + **Ответы:**
    ```json
    {
        "ok" : true
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found

## ProfileMethodsAPI

### 1. me - POST
  + **Информация об аккаунте**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
  + **Ответы:**
    ```json
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

### 2. getGroups - POST
  + **Группы**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
  + **Ответы:**
    ```json
    {
        "ok": true,
        "result": [
            1,
            -4
        ]
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found

### 3. editName - POST
  + **Редактировать имя**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **name** - новое имя (16 символов)
  + **Ответы:**
    ```json
    {
        "ok": true
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + Invalid parameters

### 4. editSurname - POST
  + **Редактировать фамилию**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **surname** - новая фамилия (может быть пустой) (16 символов)
  + **Ответы:**
    ```json
    {
        "ok": true
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found

### 5. editDescription - POST
  + **Редактировать описание**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **description** - новое описание (может быть пустой) (16 символов)
  + **Ответы:**
    ```json
    {
        "ok": true
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found

### 6. addContact - POST
  + **Добавить контакт**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **id** - индентификатор пользователя
  + **Ответы:**
    ```json
    {
        "ok": true
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + User not found
    + Contact has already been added

### 7. deleteContact - POST
  + **Удалить контакт**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **id** - индентификатор пользователя
  + **Ответы:**
    ```json
    {
        "ok": true
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + Contact not found

### 8. getUser - POST
  + **Получить пользователя**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **id** - индентификатор пользователя
  + **Ответы:**
    ```json
    {
        "ok": true, 
        "result": {
            "_id": 2, 
            "description": null, 
            "name": "Кирилл", 
            "surname": null
        }
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + User not found

### 9. getChat - POST
  + **Получить чат**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **id** - индентификатор пользователя
  + **Ответы:**
    ```json
    {
        "ok": true, 
        "result": {
            "_id": -1, 
            "admins": [
                1
            ], 
            "description": null, 
            "is_private": true, 
            "link": null, 
            "name": "Избранное", 
            "participants": [
                1
            ]
        }
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + User not found

## GroupsMethodsAPI

### 1. createGroup - POST
  + **Создать группу**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **name** - название группы
    + **link (опционально)** - ссылка на группу
    + **description (опционально)** - описание группы
  + **Ответы:**
    ```json
    {
        "ok": true, 
        "result": {
            "_id": -4, 
            "admins": [
                1
            ], 
            "description": null, 
            "is_private": false, 
            "link": null, 
            "name": "Чат", 
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

### 2. joinGroup - POST
  + **Войти в группу**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **id_group** - айди группы
  + **Ответы:**
    ```json
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
    + Invalid parameters
    + Group not found
    + Private group
    + You are already in a group

### 3. leaveGroup - POST
  + **Выйти из группы**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **id_group** - айди группы
  + **Ответы:**
    ```json
    {
        "ok": true
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + Invalid parameters
    + Group not found
    + Private group
    + You are already in a group

### 4. deleteGroup - POST
  + **Удалть группу**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **id_group** - айди группы
  + **Ответы:**
    ```json
    {
        "ok": true
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + Invalid parameters
    + Group not found
    + Private group
    + You are already in a group
    + You have no right

### MessagesMethodsAPI

### 1. sendMessage - POST
  + **Отправить сообщение в чат**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **chat** - айди чата
    + **text** - текст сообщения (2048 символов)
  + **Ответы:**
    ```json
    {
        "ok": true, 
        "result": {
            "_id": 4, 
            "date": "Thu, 04 Nov 2021 23:42:18 GMT", 
            "from_id": 1, 
            "text": "Привет"
        }
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + Chat not found
    + Private group
    + You are not in this group
    + Invalid parameters

### 2. getMessages - POST
  + **Получить список сообщений чата**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **chat** - айди группы
    + **offset** - смещение (0 по умолчанию)
    + **limit** - лимит (100 по умолчанию)
  + **Ответы:**
    ```json
    {
        "ok": true, 
        "result": [
            {
                "_id": 1, 
                "date": "Thu, 04 Nov 2021 21:09:53 GMT", 
                "from_id": 1, 
                "text": "Сохраняй сюда сообщения друг)))"
            }
        ]
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + Chat not found
    + Private group
    + You are not in this group
    + Invalid parameters

### 3. deleteMessage - POST
  + **Удалить сообщение в чате**
  + **Параметры - application/json**
    + **token** - токен сессии (32 символа)
    + **chat** - айди группы
    + **id** - айди сообщения
  + **Ответы:**
    ```json
    {
        "ok": true
    }
    ```
  + **Ошибки:**
    + Session is not authorized
    + Session not found
    + Chat not found
    + Private group
    + You are not in this group
    + Invalid parameters
    + Message not found