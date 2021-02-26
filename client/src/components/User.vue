<template>
<div>
    <table>
        <th>Login</th>
        <th>Vorname</th>
        <th>Nachname</th>
        <th>Rolle</th>
        <tr>
            <td>{{ userData.login }}</td>
            <td>{{ userData.vorname }}</td>
            <td>{{ userData.nachname }}</td>
            <td>{{ userData.rolle }}</td>
        </tr>
    </table>
    <p>userData: {{ userData }} </p>
</div>
</template>

<script>

export default {
  props: ['loginOK', 'userData'],
  data() {
    return {
    };
  },
  methods: {
  },

};
</script>
