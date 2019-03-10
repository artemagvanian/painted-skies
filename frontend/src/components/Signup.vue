<template>
    <v-container fluid fill-height>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md4>
                <v-card class="elevation-12">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Зареєструйтеся</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-form>
                            <v-text-field prepend-icon="person" name="login" label="Логін"
                                          type="text" v-model="username"></v-text-field>
                            <v-text-field id="password1" prepend-icon="lock" name="password1" label="Пароль"
                                          type="password" v-model="password1"></v-text-field>
                            <v-text-field id="password2" prepend-icon="lock" name="password2" label="Повторіть пароль"
                                          type="password" v-model="password2"></v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="onSubmit">Зареєструватися</v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
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
            async onSubmit() {
                let result = await Auth.signup(this.username, this.password1, this.password2);
                if (result) {
                    this.$router.push('/');
                }
            }
        }
    }
</script>