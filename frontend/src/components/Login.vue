<template>
    <v-container fluid fill-height>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md4>
                <v-card class="elevation-12">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Увійдіть до системи</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-form>
                            <v-text-field prepend-icon="person" name="login" label="Логін"
                                          type="text" v-model="username"></v-text-field>
                            <v-text-field id="password" prepend-icon="lock" name="password" label="Пароль"
                                          type="password" v-model="password"></v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="onSubmit">Увійти</v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
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
            async onSubmit() {
                let response = await Auth.login(this.username, this.password);
                if (response) {
                    this.$session.start();
                    this.$session.set('jwt', response);
                    this.$router.push('/')
                }
            }
        }
    }
</script>