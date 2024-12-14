import { important_offers } from "/scripts/variables.js";

export default class Offers {
    constructor(offers) {
        this.offers = this.getOffersLogoes(offers);
    }

    getOffersLogoes(offers) {
        offers.map((offer) => {
            important_offers.includes(offer.name) ? offer.logo = `../img/offers_icons/svg/${offer.name}.svg` : offer.logo = null;
        });
        return offers;
    }

    getAllOffers() {
        return this.offers;
    }

    // NEED: a full list of services in the DB
    // only important services are shown on the main card component and use a logo
    /*
    important services:
    - kanopy
    - hoopla
    - criterionchannel
    - prime
    - amazon
    - youtube
    - netflix
    - hbo
    - itunes
    */
    filterImportant() {
        return this.offers.filter(o => o.logo !== null);
    }
}
