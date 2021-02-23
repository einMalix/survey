<template>
<div>
    <form>
    Login <input name="login" type="text" v-model="newLogin" />
    <br>
    Passwort <input name="passwort" type="password" v-model="newPasswort" />
    <br>
    Vorname <input name="vorname" type="text" v-model="newVorname" />
    <br>
    Nachname <input name="nachname" type="text" v-model="newNachname" />
    <br>
    <br>
    <fieldset>
    <label>
        <input type="radio" name="rolle" value="Administrator" v-model="newRolle" />
        Administrator
    </label>
    <br>
    <label>
        <input type="radio" name="rolle" value="Kursleiter" v-model="newRolle" />
        Kursleiter
    </label>
    </fieldset>
    <button v-on:click="onSubmit()">Hinzufügen</button>
    </form>
    <br>
 <table>
    <thead>
    <tr>
        <th>Login</th>
        <th>Vorname</th>
        <th>Nachname</th>
        <th>Rolle</th>
        <th>Passwort</th>
    </tr>
    </thead>
    <tbody>
        <tr v-for="user in users" :key="user">
            <td>{{ user[0] }}</td>
            <td>{{ user[1] }}</td>
            <td>{{ user[2] }}</td>
            <td>{{ user[3] }}</td>
            <td>{{ user[4] }}</td>
            <td>
                <div>
                  <button type="button"
                  v-on:click="onEdit(user)">Ändern</button>
                  <button type="button"
                  v-on:click="onDelete(user)">Löschen</button>
                </div>
              </td>
        </tr>
    </tbody>
</table>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Liste',
  data() {
    return {
      users: '',
      newLogin: '',
      newVorname: '',
      newNachname: '',
      newRolle: '',
      newPasswort: '',
    };
  },
  methods: {
    getUsers() {
      const path = 'http://localhost:5000/liste';
      axios.get(path)
        .then((res) => {
          this.users = res.data;
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    addUser() {
      const path = 'http://localhost:5000/add';
      axios.post(path, {
        login: this.newLogin,
        vorname: this.newVorname,
        nachname: this.newNachname,
        rolle: this.newRolle,
        passwort: this.newPasswort,
      })
        .then((response) => {
        // eslint-disable-next-line
          console.log(response);
          this.getUsers();
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    onSubmit() {
      if (this.newLogin === '' || this.newVorname === '' || this.newNachname === '' || this.newRolle === '' || this.newPasswort === '') {
      // eslint-disable-next-line
        console.error(error);
      } else {
        this.addUser();
      }
    },
    removeUser(userLogin) {
      const path = `http://localhost:5000/remove/${userLogin}`;
      axios.delete(path)
        .then(() => {
          this.getUsers();
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
          this.getUsers();
        });
    },
    onDelete(user) {
      this.removeUser(user[0]);
    },
    editUser(userLogin) {
      const path = `http://localhost:5000/edit/${userLogin}`;
      axios.put(path, {
        login: this.newLogin,
        vorname: this.newVorname,
        nachname: this.newNachname,
        rolle: this.newRolle,
        passwort: this.newPasswort,
      })
        .then(() => {
          this.getUsers();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getUsers();
        });
    },
    onEdit(user) {
      if (this.newLogin === '' && this.newVorname === '' && this.newNachname === '' && this.newRolle === '' && this.newPasswort === '') {
      // eslint-disable-next-line
        console.error(error);
      } else {
        this.editUser(user[0]);
      }
    },
  },
  created() {
    this.getUsers();
  },
};
</script>
