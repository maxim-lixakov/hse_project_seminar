const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
let good_id = urlParams.get('id')
export default {
    good_id
};
