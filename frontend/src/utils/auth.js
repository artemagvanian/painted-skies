import $ from 'jquery'

export default {
    login(session, username, password, router) {
        $.ajax({
            url: '/api/auth/obtain_token',
            method: 'POST',
            data: {
                password, username
            }
        }).then((response) => {
            session.start();
            session.set('jwt', response.token);
            router.push('/');
        }).catch((err) => {
            console.log('Error: ', err);
        })
    },
    logout(session, router) {
        session.destroy();
        router.push('/');
    },
}