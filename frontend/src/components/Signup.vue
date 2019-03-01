<template>
    <div id="signup">
        <b-container class="d-flex justify-content-center flex-column h-100">
            <h1 class="text-center mb-5">Зареєструйтесь</h1>
            <b-row class="text-center w-100">
                <b-form @submit="onSubmit" class="mx-auto">
                    <b-form-group id="usernameInputGroup"
                                  label-for="usernameInput"
                                  description="Введіть ваш новий логін">
                        <b-form-input id="usernameInput"
                                      type="text"
                                      v-model="username"
                                      required
                                      placeholder="Введіть логін">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="password1InputGroup"
                                  label-for="password1Input"
                                  description="Введіть ваш новий суперсекретний пароль">
                        <b-form-input id="password1Input"
                                      type="password"
                                      v-model="password1"
                                      required
                                      placeholder="Введіть пароль">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="password2InputGroup"
                                  label-for="password2Input"
                                  description="Повторіть ваш новий суперсекретний пароль">
                        <b-form-input id="password2Input"
                                      type="password"
                                      v-model="password2"
                                      required
                                      placeholder="Повторіть пароль">
                        </b-form-input>
                    </b-form-group>
                    <b-button type="submit" variant="primary" class="btn-block">Зарєструватися</b-button>
                </b-form>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    import Auth from '../utils/auth'

    export default {
        name: "Signup",
        data() {
            return {
                username: "",
                password1: "",
                password2: "",
            }
        },
        methods: {
            onSubmit(e) {
                e.preventDefault();
                Auth.signup(this.username, this.password1, this.password2, this.$router)
            }
        }
    }
</script>

<style scoped>
    #signup {
        height: 100%;
    }
</style>