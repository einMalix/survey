<template>
<div>
  <div class="AddUser">
  <button v-on:click="onClickButtonAddUser"
    v-if="hideAddUserButton == false">Nutzer hinzufügen</button>
    <div v-if="showAddUserForm">
    <form>
    <label for="login">Login</label><br>
    <input name="login" id="login" type="text" v-model="newLogin" autocomplete="off"/><br>
    <label for="password">Passwort</label><br>
    <input name="passwort" id="password" type="password"
    v-model="newPasswort" autocomplete="off"/><br>
    <label for="vorname">Vorname</label><br>
    <input name="vorname" id="vorname" type="text" v-model="newVorname" autocomplete="off"/><br>
    <label for="nachname">Nachname</label><br>
    <input name="nachname" id="nachname" type="text" v-model="newNachname" autocomplete="off"/><br>
    <fieldset>
    <label>
        <input type="radio" id="admin" name="rolle" value="Administrator" v-model="newRolle" />
        <label for="admin"> Administrator</label><br>
    </label>
    <label>
        <input type="radio" id="leiter" name="rolle" value="Kursleiter" v-model="newRolle" />
        <label for="leiter">Kursleiter</label><br>
    </label>
    </fieldset>
    <button v-on:click.prevent="onSubmit()">Hinzufügen</button>
    <button v-on:click="AddUserOnCancel">Abbrechen</button>
    </form>
    </div>
    </div>
    <div class="UserList">
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
    <tbody class="UserTable" v-for="user in users" :key="user">
        <tr class="User">
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
</div>
</template>

<script>
import axios from 'axios';

const crypto = require('crypto');

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
      hideAddUserButton: false,
      showAddUserForm: false,
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
      const hashPW = crypto.createHash('sha1').update(this.newPasswort).digest('hex');
      axios.post(path, {
        login: this.newLogin,
        vorname: this.newVorname,
        nachname: this.newNachname,
        rolle: this.newRolle,
        passwort: hashPW,
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
      const hashPW = crypto.createHash('sha1').update(this.newPasswort).digest('hex');
      axios.put(path, {
        login: this.newLogin,
        vorname: this.newVorname,
        nachname: this.newNachname,
        rolle: this.newRolle,
        passwort: hashPW,
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
    onClickButtonAddUser() {
      this.newLogin = '';
      this.newVorname = '';
      this.newNachname = '';
      this.newRolle = '';
      this.newPasswort = '';
      this.showAddUserForm = true;
      this.hideAddUserButton = true;
    },
    AddUserOnCancel() {
      this.showAddUserForm = false;
      this.hideAddUserButton = false;
    },
  },
  created() {
    this.getUsers();
  },
};
</script>

<style scoped>
  .AddUser {
    padding: 20px;
  }
  .UserList {
    padding: 20px;
  }
  .User {
    border: 2px solid black;
  }
</style>
