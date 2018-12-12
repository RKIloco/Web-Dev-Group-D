new Vue({
    el: '#about',
    data: {
    },
    mounted: function() {
        logged = localStorage.getItem('loggedin')
        if (logged == null){
            window.location.href = '/login.html'
        }
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