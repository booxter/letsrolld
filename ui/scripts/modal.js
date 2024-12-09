export default class Modal {
    constructor(title, trailer_url, offers) {
        this.title = title;
        this.trailer_url = trailer_url;
        this.offers = offers;
    }

    // extract YouTube movie id from the link
    getYouTubeId(url) {
        const movieYouTubeId = url.replace("https://www.youtube.com/watch?v=", "");
        return movieYouTubeId;
    }

    fillInModal() {
        const title = document.querySelector(".modal-title");
        title.textContent = this.title;

        const body = document.querySelector(".modal-body");

        if (this.trailer_url) {
            const trailer_id = this.getYouTubeId(this.trailer_url);
            // compose embed link for the trailer
            const trailer = this.createTrailer(`https://www.youtube.com/embed/${trailer_id}`);
            body.appendChild(trailer);
        }
        // TODO: reuse createLinkElement() from movie.js module (move it to the separate utility module first)
        // BUG: links not clearing when modal is closed
        if (this.offers) {
            console.log(this.offers);
            const offerLinks = document.createElement("div");
            offerLinks.classList.add("offers-all");
            this.offers.map(o => {
                const linkElem = document.createElement('a');
                if (o.url !== null) {
                    linkElem.setAttribute("href", o.url);
                    linkElem.setAttribute("target", "_blank");
                }
                linkElem.classList.add("movie-link");
                linkElem.classList.add(`movie-link-${o.name}`);
                const linkText = document.createElement("span");
                linkText.classList.add("title-link");
                linkText.innerText = o.name;
                linkElem.appendChild(linkText);
                offerLinks.appendChild(linkElem);
            });
            body.appendChild(offerLinks);
        }

        this.openModal();

        const closeBtn = document.querySelector(".closeBtn");
        closeBtn.addEventListener("click", this.closeModal.bind(this));

        window.addEventListener('click', (e) => this.closeModalOutside(e));
    }

    createTrailer (url) {
        const trailer = document.createElement("iframe");
        trailer.setAttribute("width", "100%");
        trailer.setAttribute("height", "100%");
        trailer.setAttribute("src", url);
        trailer.setAttribute("title", this.title);
        trailer.setAttribute("frameborder", "0");
        trailer.setAttribute("allowfullscreen", true);
        trailer.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");

        return trailer;
    }

    openModal() {
        const modal = document.getElementById("modal");
        modal.style.display = "block";
    }

    closeModal() {
        const modal = document.getElementById("modal");
        modal.classList.toggle("show-modal");
        modal.style.display = "none";
        this.stopVideos();
        const offersEl = document.querySelector(".modal-body");
        offersEl.innerHTML = null;
        this.offers = null;
        console.log(this.offers);
    }

    closeModalOutside(e) {
        const targetElem = e.target.getAttribute("class");
        const modalItem = document.getElementById("modal");
        // console.log(targetElem);
        if(targetElem === "modal") {
            modalItem.style.display = "none";
            this.stopVideos();
            const offersEl = document.querySelector(".modal-body");
            offersEl.innerHTML = null;
            this.offers = null;
        }
    }

    stopVideos() {
        const trailers = document.querySelectorAll("iframe");
        trailers.forEach(trailer => {
            trailer.src = "";
            trailer.remove();
        })
    }
}
