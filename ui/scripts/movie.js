import Modal from "/scripts/modal.js";
import Offers from "/scripts/offers.js";
import { important_offers } from "/scripts/variables.js";

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
        /*
        keys: name, url, logo
        logo can be url (string) or null
        */
        this.offers = offers;
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

            cover.addEventListener("click", () => new Modal(this.title, this.trailer_url, null).fillInModal());
        }

        movieLeft.appendChild(cover);

        // other services -> open in modal, simple list with no logos
        if (this.offers.length > 0) {
            const movie_offers = new Offers(this.offers);

            const movie_offers_all = movie_offers.getAllOffers();
            console.log(`All offers from Offers class: ${movie_offers_all.length}`);
            // movie_offers_all.map(o => console.log(o));

            const movie_offers_important = movie_offers.filterImportant();
            console.log(`Important offers from Offers class: ${movie_offers_important.length}`);

            // TODO: rename function to getOffersElement
            const offers_el = this.getOffers(movie_offers_important, "movie-offers-list");

            const offers = document.createElement('div');
            offers.classList.add("offers");

            // console.log(`my_offers: ${movie_important_offers.length}, all_offers: ${this.offers.length}`);

            // if we have non-important offers
            if (offers_el) {
                offers.appendChild(offers_el);

                // console.log(`Offers_el number of childs:${offers_el.childNodes.length}`);

                if (movie_offers_important.length < movie_offers_all.length) {
                    // TODO: make reusable
                    const moreLink = this.createLinkElem(null, "show_more", "show more →");
                    moreLink.addEventListener("click", () => new Modal("Where to watch", null, movie_offers_all).fillInModal());
                    offers.appendChild(moreLink);
                }
            } else {
                const moreLink = this.createLinkElem(null, "show_more", "where to watch →");
                moreLink.addEventListener("click", () => new Modal("Where to watch", null, movie_offers_all).fillInModal());
                offers.appendChild(moreLink);
            }
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
        const movieInfoContainer = document.createElement('div');
        movieInfoContainer.classList.add("movie-info");

        const title = this.createMovieElemText("h1", "movie-title", this.title);
        const year = this.createMovieElemText("h2", "movie-year", this.year);
        const director = this.createDirectorsList(this.directors.map(d => d.name));
        const rating = this.createMovieElemText("h3", "movie-rating", this.rating);
        const runtime = this.createMovieElemText("h4", "movie-runtime", this.runtime? `${this.runtime} min` : "");
        const description = this.createMovieElemText("p", "movie-description", this.description);
        const genres = this.createListWithTitle("genres", this.genres);
        const counries = this.createListWithTitle("countries", this.countries);
        const links = this.getLinks();

        movieInfoContainer.appendChild(title);
        movieInfoContainer.appendChild(year);
        movieInfoContainer.appendChild(director);
        movieInfoContainer.appendChild(rating);
        movieInfoContainer.appendChild(runtime);
        movieInfoContainer.appendChild(description);
        movieInfoContainer.appendChild(genres);
        movieInfoContainer.appendChild(counries);
        movieInfoContainer.appendChild(links);

        return movieInfoContainer;
    }

    createDirectorsList(names) {
        const container = document.createElement('h2');
        container.classList.add("movie-directors");

        if(names) {
            let dirNamesStr = names.map(String).join(', ');
            let result = `Directed by <span class="directors-names">${dirNamesStr}</span>`;
            container.innerHTML = result;
        }

        return container;
    }

    createListWithTitle(name, data) {
        const container = document.createElement('div');
        container.classList.add(name);

        const titleUpper = name.charAt(0).toUpperCase() + name.slice(1);

        if(data !== "") {
            const title = this.createMovieElemText("h3", `${name}-title`, `${titleUpper}:`);
            container.appendChild(title);
            container.appendChild(data);
        }

        return container;
    }

    // expects countries object that has name and flag fields, class
    getFlags(countries, name) {
        let flags = "";

        if (countries.length == 0) {
            return flags;
        }

        const list = document.createElement("ul");
        list.classList.add(name);

        countries.map(({flag, name} = country) => {
            // &#127987; adds white flag symbol as a default flag
            flag = flag || "&#127987;";
            flags += `<li class="country-flag">${flag}<span class="country-name-tooltip">${name}</span></li>`;
        })
        list.innerHTML = flags;
        return list;
    }

    // TODO: move this into separate module
    // expects offers object that has name and url fields
    getOffers(offers, name) {
        const offersList = document.createElement("div");
        offersList.classList.add(name);

        offers.map(({name, url, logo} = offer) => {
            const link = this.createLinkElem(url, "offer", null);

            // add icon to the link
            const icon = document.createElement("span");
            icon.classList.add("brand-icon");
            icon.innerHTML = `<img id="svg-${name}" src=${logo} class="logo-img logo-${name} alt="Logo for ${name} streaming service" />`;
            const tooltip = document.createElement("span");
            tooltip.classList.add("offer-name-tooltip");
            tooltip.innerText = name;
            link.appendChild(icon);
            link.appendChild(tooltip);

            offersList.appendChild(link);
        })

        if (offersList.childNodes.length === 0) {
            return null
        }

        return offersList;
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

        if(text) {
            const linkText = document.createElement("span");
            linkText.classList.add("title-link");
            linkText.innerText = text;
            linkElem.appendChild(linkText);
        }

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
