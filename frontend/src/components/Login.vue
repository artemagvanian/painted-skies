<template>
    <div id="login">
        <b-container class="d-flex justify-content-center flex-column h-100">
            <h1 class="text-center mb-5">Увійдіть до системи</h1>
            <b-row class="text-center w-100">
                <b-form @submit="onSubmit" class="mx-auto">
                    <b-form-group id="usernameInputGroup"
                                  label-for="usernameInput"
                                  description="Введіть логін, який ви використовували при реєстрації">
                        <b-form-input id="usernameInput"
                                      type="text"
                                      v-model="username"
                                      required
                                      placeholder="Введіть логін">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="passwordInputGroup"
                                  label-for="passwordInput"
                                  description="Введіть ваш суперсекретний пароль">
                        <b-form-input id="passwordInput"
                                      type="password"
                                      v-model="password"
                                      required
                                      placeholder="Введіть пароль">
                        </b-form-input>
                    </b-form-group>
                    <b-button type="submit" variant="primary" class="btn-block">Увійти</b-button>
                </b-form>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    import Auth from '../utils/auth'

    export default {
        name: "Login",
        data() {
            return {
                username: "",
                password: "",
            }
        },
        methods: {
            onSubmit(e) {
                e.preventDefault();
                Auth.login(this.$session, this.username, this.password, this.$router)
            }
        }
    }
</script>

<style scoped>
    #login {
        height: 100%;
    }
</style>