new Vue({
    el: '#buy',
    data: {
        items: [],
        bought_id: null,
        message: null,
    },
    mounted: function() {
        axios({
            method: 'get',
            url: '/api/items'
        })
        .then(response => {
            this.items = response.data
        })
    },
    methods: {
        buyItem() {
            axios.post('/api/buyid',
            {
                bought_id: this.bought_id,
            })
            .then(response => {
                if (response.data == "") {
                    localStorage.setItem('bought_id', this.bought_id)
                    window.location.href = '/buyitem.html'
                } else {
                    this.message = response.data
                }
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