const messages = {
    en: {
        drawer: {
            takeNotesFromPdf: 'Take notes from PDF',
            takeNotesFromPicture: 'Take notes from picture',
            takeNotesFromScratch: 'Create notes from scratch',
            library: 'Library',
            signUp: 'Sign up',
            login: 'Login',
            logout: 'Logout',
        },
        serverErrorMessage: {
            title: 'An error occurred!',
            shortText: 'An error occurred! Try to refresh the page!',
            text: 'An error occurred! Try to refresh the page!',
        },
        classroom: {
            selectNotesForComparison: 'Select notes for comparison',
            selectGroup: 'Select student\'s group',
            selectStudent: 'Select student',
            selectStudentNotes: 'Select student\'s notes',
            selectTeacherNotes: 'Select your own notes',
            compare: 'Compare',
            similarityIndex: 'Similarity index'
        },
        languages: {
            ukrainian: 'Ukrainian',
            russian: 'Russian',
            english: 'English'
        },
        uploader: {
            uploadFile: 'Upload file',
            clickToSelectImage: 'Click to upload picture',
            clickToSelectDocument: 'Click to upload document',
            selectFirstPage: 'Select first page of notes',
            selectLastPage: 'Select last page of notes',
            selectLanguage: 'Select language of notes',
            start: 'Start!'
        },
        auth: {
            loginTitle: 'Login to the system',
            signUpTitle: 'Sign up',
            username: 'Username',
            password: 'Password',
            login: 'Login',
            signUp: 'Sign up',
            repeatPassword: 'Repeat password',
        },
        list: {
            edited_at: 'Edited',
            created_at: 'Created',
            edit: 'Edit'
        },
        editor: {
            title: 'Title',
            addNode: 'Add node',
            addEdge: 'Add edge',
            nodeLabel: 'Node text',
            deleteNode: 'Delete node',
            selectNode: 'Select node to edit',
            saving: 'Saving...',
            saved: 'Saved',
            notSaved: 'Not saved',
            basicTitle: 'New notes',
        },
        menu: {
            welcome: 'Welcome!',
            intro: '<p>Open right drawer to start working with the system</p>' +
                '<p>Interactive guide will be available soon</p>'
        }
    },
    uk: {
        drawer: {
            takeNotesFromPdf: 'Конспектувати з PDF',
            takeNotesFromPicture: 'Конспектувати з картинки',
            takeNotesFromScratch: 'Створити конспект з нуля',
            library: 'Бібліотека',
            signUp: 'Зареєструватися',
            login: 'Увійти',
            logout: 'Вийти',
        },
        serverErrorMessage: {
            title: 'Сталася помилка!',
            shortText: 'Сталася помилка! Спробуйте оновити сторінку!',
            text: 'Вся команда розробників вже знає про це та намагається все виправити. Зверніть увагу, що наш сервер не оброблює зображення, більші за 10 МБ. Якщо виділень на конспекті дуже багато та сервер завантажений, можуть статися помилки. Спробуйте оновити сторінку!'
        },
        classroom: {
            selectNotesForComparison: 'Виберіть конспекти для порівняння',
            selectGroup: 'Виберіть клас учня',
            selectStudent: 'Виберіть учня',
            selectStudentNotes: 'Виберіть конспект учня',
            selectTeacherNotes: 'Виберіть свій конспект',
            compare: 'Порівняти',
            similarityIndex: 'Індекс схожості'
        },
        languages: {
            ukrainian: 'Українська',
            russian: 'Російська',
            english: 'Англійська'
        },
        uploader: {
            uploadFile: 'Завантажте файл',
            clickToSelectImage: 'Натисніть, щоб вибрати зображення на комп\'ютері',
            clickToSelectDocument: 'Натисніть, щоб вибрати документ на комп\'ютері',
            selectFirstPage: 'Введіть сторінку, з якої почнете конспектувати',
            selectLastPage: 'Введіть сторінку, на якій закінчите конспектувати',
            selectLanguage: 'Виберіть мову конспектування',
            start: 'Поїхали!'
        },
        auth: {
            loginTitle: 'Увійдіть до системи',
            signUpTitle: 'Зареєструйтеся',
            username: 'Логін',
            password: 'Пароль',
            login: 'Увійти',
            signUp: 'Зареєструватися',
            repeatPassword: 'Повторіть пароль',
        },
        list: {
            edited_at: 'Змінено',
            created_at: 'Створено',
            edit: 'Редагувати'
        },
        editor: {
            title: 'Назва ментальної карти',
            addNode: 'Додати вузол',
            addEdge: 'Додати ребро',
            nodeLabel: 'Текст вузла',
            deleteNode: 'Видалити вузол',
            selectNode: 'Виберіть вузол для редагування',
            saving: 'Зберігаємо дані...',
            saved: 'Дані збережено',
            notSaved: 'Дані не збережено',
            basicTitle: 'Нова ментальна карта',
        },
        menu: {
            welcome: 'Вітаємо!',
            intro: '<p>Для початку роботи, відкрийте бокову панель кліком по елементу інтерфейсу (три смужки)</p>' +
                '<p>Інтерактивний гайд буде доступний згодом</p>' +
                '<p>Для отримання додаткової інформації про розробника, клікніть по літері І біля трьох смужок</p>'
        }
    }
};

export default messages;