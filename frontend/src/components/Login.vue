<template>
    <v-container fill-height fluid>
        <v-layout align-center justify-center>
            <v-flex md4 sm8 xs12>
                <v-card class="elevation-12">
                    <v-toolbar color="primary" dark>
                        <v-toolbar-title>Увійдіть до системи</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-form>
                            <v-text-field label="Логін" name="login" prepend-icon="person"
                                          type="text" v-model="username"></v-text-field>
                            <v-text-field id="password" label="Пароль" name="password" prepend-icon="lock"
                                          type="password" v-model="password"></v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn @click="onSubmit" color="primary">Увійти</v-btn>
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
                let response = await Auth.obtainToken(this.username, this.password);
                if (response) {
                    this.$router.push('/')
                }
            }
        }
    }
</script>