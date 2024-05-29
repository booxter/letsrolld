import Modal from "/scripts/modal.js";

export default class Movie {
    constructor(title, description, year, rating, runtime, lb_url, jw_url, trailer_url, genres, countries, offers, directors) {
        this.title = title;
        this.description = description;
        this.year = year;
        this.rating = rating;
        this.runtime = runtime;
        this.lb_url = lb_url;
        this.jw_url = jw_url;
        this.trailer_url = trailer_url;
        this.genres = this.getListHTML(genres, "movie-genres-list");
        // TODO: handle null flag
        this.countries = this.getListHTML(countries.map(c => c.flag + " " + c.name), "movie-countries-list");
        // TODO: expose urls
        // this.offers = this.getListHTML(offers.map(o => o.name), "movie-offers-list");
        this.offers = this.getOffers(offers, "movie-offers-list");
        this.directors = directors;
        this.cover_url = "img/movie_temp.jpg";
    }

    createFullMovie() {
        const movieEl = document.createElement("div");
        movieEl.classList.add("movie-card");

        const leftSide = this.createLeftSide();
        const rightSide = this.createRightSide();


        movieEl.appendChild(leftSide);
        movieEl.appendChild(rightSide);

        return movieEl;
    }

    createLeftSide() {
        const movieLeft = document.createElement("div");
        movieLeft.classList.add("movie-left");

        // TODO: change for the dynamic image cover later
        const imageElem = `<img class="movie-image-cover" src=${this.cover_url} alt="Watch this space, cover is comming soon" />`;
        const cover = this.createMovieElemHTML('figure', 'movie-image', imageElem);
        
        // handle the case if trailer is not available
        if (this.trailer_url) {
            //the html character code is an arrow directed to the right
            const imgCaption = this.createMovieElemHTML("figcaption", "movie-image-caption", "Trailer &#10162;");
            cover.appendChild(imgCaption);

            cover.addEventListener("click", () => new Modal(this.title, this.trailer_url).fillInModal());
        }

        movieLeft.appendChild(cover);

        if (this.offers) {
            const offers = document.createElement('div');
            offers.classList.add("offers");
            offers.appendChild(this.offers);
            movieLeft.appendChild(offers);
        }

        return movieLeft;
    }

    createRightSide() {
        const movieRight = document.createElement("div");
        movieRight.classList.add("movie-right");

        const info = this.createFullMovieInfo();

        movieRight.appendChild(info);

        return movieRight;
    }

    createFullMovieInfo() {
        const movieInfoConteiner = document.createElement('div');
        movieInfoConteiner.classList.add("movie-info");

        const title = this.createMovieElemText("h1", "movie-title", this.title);
        const year = this.createMovieElemText("h2", "movie-year", this.year);
        const rating = this.createMovieElemText("h3", "movie-rating", this.rating);
        const runtime = this.createMovieElemText("h4", "movie-runtime", this.runtime? `${this.runtime} min` : "");
        const description = this.createMovieElemText("p", "movie-description", this.description);
        const genres = this.createListWithTitle("genres", this.genres);
        const counries = this.createListWithTitle("countries", this.countries);
        const links = this.getLinks();

        movieInfoConteiner.appendChild(title);
        movieInfoConteiner.appendChild(year);
        movieInfoConteiner.appendChild(rating);
        movieInfoConteiner.appendChild(runtime);
        movieInfoConteiner.appendChild(description);
        movieInfoConteiner.appendChild(genres);
        movieInfoConteiner.appendChild(counries);
        movieInfoConteiner.appendChild(links);

        return movieInfoConteiner;
    }

    createListWithTitle(name, data) {
        const conteiner = document.createElement('div');
        conteiner.classList.add(name);

        const titleUpper = name.charAt(0).toUpperCase() + name.slice(1);

        if(data !== "") {
            const title = this.createMovieElemText("h3", `${name}-title`, `${titleUpper}:`);
            conteiner.appendChild(title);
            conteiner.appendChild(data);
        }

        return conteiner;
    }

    // TODO: move this into separate module
    // TODO: make list of offers shorter by default, then add add an option to expand list in modal window 
    // expects offers object that has name and url fields
    getOffers(offers, name) {
        const offersList = document.createElement("div");
        offersList.classList.add(name);

        if (offers.length == 0) {
            return "";
        }

        // NEED: a full list of services in the DB
        // TODO: check if the service has a matching logo, if not - use a placeholder logo
        offers.map(({name, url} = offer) => {
            const link = this.createLinkElem(url, "offer", name);
            // add icon to the link
            // TODO: add icons for different services (SVG?)
            // TODO: for now it shows only couple of icons, should add icons source for everything
            const icon = document.createElement("span");
            icon.classList.add("brand-icon");
            
            const logoName = this.getSvg(name);

            console.log(`name: ${name}, logoName: ${logoName}`);
            
            icon.innerHTML = `<img id="svg-${name}" src="../img/offers_icons/${logoName}" class="logo-img logo-${name} alt="Logo for ${name} streaming service" />`;
            link.appendChild(icon);

            offersList.appendChild(link);
        })

        return offersList;
    }

    // TODO: expend checks for services other then physical
    getSvg(name) {
        return name === "physical" ? name = "png/buy.png" : `svg/${name}.svg`;
    }

    getListHTML(arr, name) {
        let result = "";

        if (arr.length !== 0) {
            const list = document.createElement("ul");
            list.classList.add(name);

            for(let i=0; i<arr.length; i++) {
                result += `<li>${arr[i]}</li>`;
            }
            list.innerHTML = result;
            return list;
        } else {
            return result;
        }
    }

    getLinks() {
        const links_container = document.createElement("div");
        links_container.classList.add("links");

        if(this.lb_url) {
            const lb_button = this.createButtonElem(["btn", "btn--link"]);
            const lb_link = this.createLinkElem(this.lb_url, "letterboxd", "Letterboxd");
            lb_button.appendChild(lb_link);
            links_container.appendChild(lb_button);
        }

        if (this.jw_url) {
            const jw_button = this.createButtonElem(["btn", "btn--link"]);
            const jw_link = this.createLinkElem(this.jw_url, "just_watch", "JustWatch");
            jw_button.appendChild(jw_link);
            links_container.appendChild(jw_button);
        }

        return links_container;
    }

    // arg: list of strings with class names
    createButtonElem(classes) {
        const button = document.createElement("button");
        classes.forEach(c => {
            button.classList.add(c);
        })

        return button;
    }

    createLinkElem(link, name, text) {
        const linkElem = document.createElement('a');

        // url can be null (the most common example: a physical offer)
        if (link !== null) {
            linkElem.setAttribute("href", link);
            linkElem.setAttribute("target", "_blank");
        }

        linkElem.classList.add("movie-link");
        linkElem.classList.add(`movie-link-${name}`);

        const linkText = document.createElement("span");
        linkText.classList.add("title-link");
        linkText.innerText = text;
        linkElem.appendChild(linkText);

        return linkElem;
    }

    createMovieElemText(tag, name, text) {
        const elem = document.createElement(tag);
        elem.classList.add(name);
        elem.innerText = text;
        return elem;
    }

    createMovieElemHTML(tag, name, htmlString) {
        const elem = document.createElement(tag);
        elem.className = name;
        elem.innerHTML = htmlString;
        return elem;
    }
}
