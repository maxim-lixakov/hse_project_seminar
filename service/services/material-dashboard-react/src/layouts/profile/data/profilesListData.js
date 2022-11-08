/**
=========================================================
* Material Dashboard 2 React - v2.1.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-dashboard-react
* Copyright 2022 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

// Images
import max from "assets/images/max1.jpeg";
import ilyas from "assets/images/ilyas.jpeg";
import empty from "assets/images/empty.jpg";
// import roma from "assets/images/max.jpeg";
// import artem from "assets/images/max.jpeg";
// import semyon from "assets/images/max.jpeg";

export default [
  {
    image: max,
    name: "Ликсаков Максим",
    description: "разработчик",
    action: {
      type: "internal",
      route: "/pages/profile/profile-overview",
      color: "info",
      label: "mvliksakov@edu.hse.ru",
    },
  },
  {
    image: ilyas,
    name: "Гасанов Ильяс",
    description: "разработчик",
    action: {
      type: "internal",
      route: "/pages/profile/profile-overview",
      color: "info",
    },
  },
  {
    image: empty,
    name: "Зарьянов Роман",
    description: "аналитик",
    action: {
      type: "internal",
      route: "/pages/profile/profile-overview",
      color: "info",
    },
  },
  {
    image: empty,
    name: "Ордин Семен",
    description: "аналитик",
    action: {
      type: "internal",
      route: "/pages/profile/profile-overview",
      color: "info",
    },
  },
  {
    image: empty,
    name: "Федонин Артем",
    description: "бизнес-аналитик",
    action: {
      type: "internal",
      route: "/pages/profile/profile-overview",
      color: "info",
    },
  },
];
