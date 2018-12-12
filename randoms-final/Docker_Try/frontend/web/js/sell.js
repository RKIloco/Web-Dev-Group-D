new Vue({
    el: '#sell',
    data: {
        name: null,
        price: null,
        image: null,
        message: null,
    },
    mounted: function() {
        logged = localStorage.getItem('loggedin')
        if (logged == null){
            window.location.href = '/login.html'
        }
    },
    methods: {
        sellItem() {
            axios.post('/api/sell',
            {
                name: this.name,
                price: this.price,
                image: this.image,
            })
            .then(response => {
                this.message = response.data
            })
        },
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