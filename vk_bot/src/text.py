"""
Модуль для хранения текстовых сообщений
"""
WELCOME_BACK = "Добро пожаловать обратно!\nГлавное меню {role_text}:"
WELCOME_NEW_USER = (
    "Добро пожаловать! Пожалуйста, пройдите регистрацию.\nВыберите роль:"
)
ROLE_PARENT = "родителя"
ROLE_LOGOPED = "логопеда"
PARENT_ROLE = "родитель"
LOGOPED_ROLE = "логопед"
SELECT_ROLE_ERROR = "Пожалуйста, выберите роль из предложенных."
ROLE_REGISTERED = (
    "Ваша роль {role} зарегистрирована, вы можете её сменить в главном меню."
)
MAIN_MENU = "Главное меню:"
ROLE_REGISTER_ERROR = (
    "Произошла ошибка при регистрации роли. Попробуйте снова."
)
CHANGE_ROLE_PROMPT = "Выберите новую роль:"
ASK_QUESTION_PROMPT = "Пожалуйста, напишите ваш вопрос или нажмите 'Отменить':"
CANCEL = "Отменить"
TO_LOGOPED = "логопеду"
TO_DIRECTOR = "руководителю"
NO_DESCRIPTION = "Описание отсутствует"
COMMAND_NOT_FOUND = "Произошла ошибка, команда не найдена."
FILE_NOT_FOUND = "Не удалось найти файл."
ATTACHMENT_NOT_FOUND = "Произошла ошибка, вложение не найдено."
SELECT_NEXT_ACTION = "Выберите следующее действие:"
QUESTION_SENT = "Ваш вопрос отправлен {role}."
QUESTION_SEND_ERROR = (
    "Произошла ошибка при отправке вопроса. Попробуйте снова."
)
ANSWER_TEMPLATE = (
    "Здравствуйте!\n"
    "Ваш вопрос:\n{question_text}\n\n"
    "Ответ:\n{answer_text}"
)
RETURNING_TO_MENU = "Возвращение в главное меню {role_text}"
RETURN_TO_MENU_ERROR = "Произошла ошибка. Попробуйте снова."
MENU_UPDATED = "Меню {role_text} обновлено"
