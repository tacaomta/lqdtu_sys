document.addEventListener(

    "DOMContentLoaded",

    () => {
        new TomSelect(

        "#authorSelect",

        {

            valueField: "id",

        labelField: "text",

        searchField: "text",

        load(query, callback) {

            fetch(

                `/accounts/api/authors/search/?q=${query}`

            )

                .then(

                    r => r.json()

                )

                .then(

                    data => callback(

                        data.results

                    )

                );

            }

        }

        );


        new TomSelect(

        "#publicationSelect",

        {

            valueField: "id",

        labelField: "text",

        searchField: "text",

        plugins: [

        "remove_button"

        ],

        load(query, callback) {

            fetch(

                `/accounts/api/publications/search/?q=${query}`

            )

                .then(

                    r => r.json()

                )

                .then(

                    data => callback(

                        data.results

                    )

                );

            }

        });

        

    }
);