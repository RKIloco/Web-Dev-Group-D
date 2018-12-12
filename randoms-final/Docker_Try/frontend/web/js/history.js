new Vue({
    el: '#history',
    data: {
        items: [],
    },
    mounted: function() {
        axios({
            method: 'get',
            url: '/api/history'
        })
        .then(response => {this.items = response.data})
    },
    methods: {
        logOut() {
            axios.post('/api/logout',
            {
                logged: "0",
            })
            .then(response => {
                localStorage.clear();
                window.location.href = '/login.html'
            })
        },
    },
})