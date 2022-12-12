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
import React, { useEffect, useState } from "react";
// @mui material components
import Grid from "@mui/material/Grid";

// Material Dashboard 2 React components
import MDBox from "components/MDBox";

// Material Dashboard 2 React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import ReportsBarChart from "examples/Charts/BarCharts/ReportsBarChart";
import ReportsLineChart from "examples/Charts/LineCharts/ReportsLineChart";
import ComplexStatisticsCard from "examples/Cards/StatisticsCards/ComplexStatisticsCard";

// Data
import good_id from "layouts/dashboard/data/reportsBarChartData";
import reportsLineChartData from "layouts/dashboard/data/reportsLineChartData";

// Dashboard components
import Projects from "layouts/dashboard/components/Projects";
import OrdersOverview from "layouts/dashboard/components/OrdersOverview";

function Dashboard() {
  const { sales, tasks } = reportsLineChartData;
  const [rows, setRows] = useState("");
  const [qty, setQty] = useState("");

  useEffect(() => {
    const url = "http://217.25.88.87:1337/api/data_info";
    const fetchData = async () => {
      try {
        const response = await fetch(url);
        const json = await response.json();
        setRows(json.rows);
      } catch (error) {
        console.log("error", error);
      }
    };
    const fetchData2 = async () => {
      try {
        console.log(good_id, good_id.toString())
        const  url = `http://217.25.88.87:1337/api/get_info/${good_id.good_id}`;
        const response = await fetch(url);
        const json = await response.json();
        let qty = json.qty;
        setQty({
  labels: ["M", "T", "W", "T", "F", "S", "S"],
  datasets: { label: "кол-во товара", data: [12, 45, 46, 75, 57, 34, 57, 53]},
});
      } catch (error) {
        console.log("error", error);
      }
    };
    fetchData();
    fetchData2()
  }, []);

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox py={3}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="dark"
                icon="weekend"
                title="Записей по товару"
                count={rows}
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                icon="leaderboard"
                title="Кол-во товара на складе"
                count="2,300"
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="success"
                icon="store"
                title="Прирост кол-ва товара"
                count="34k"
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="primary"
                icon="person_add"
                title="Прирост выручки"
                count="+91"
              />
            </MDBox>
          </Grid>
        </Grid>
        <MDBox mt={4.5}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6} lg={4}>
              <MDBox mb={3}>
                <ReportsBarChart
                  color="info"
                  title="Товаров на складе"
                  description="остаток количества товара на складе"
                  date="обновлено 20.12.2022"
                  chart={qty}
                />
              </MDBox>
            </Grid>
            <Grid item xs={12} md={6} lg={4}>
              <MDBox mb={3}>
                <ReportsLineChart
                  color="success"
                  title="Выручка товара"
                  description={
                    <>
                      (<strong>+15%</strong>) прирост выручки.
                    </>
                  }
                  date="обновлено 20.12.2022"
                  chart={sales}
                />
              </MDBox>
            </Grid>
            <Grid item xs={12} md={6} lg={4}>
              <MDBox mb={3}>
                <ReportsLineChart
                  color="dark"
                  title="Прогноз выручки"
                  description="ожидаемый прогноз выручки на 7 дней"
                  date="обновлено 20.12.2022"
                  chart={tasks}
                />
              </MDBox>
            </Grid>
          </Grid>
        </MDBox>
        <MDBox>
        </MDBox>
      </MDBox>
      <Footer />
    </DashboardLayout>
  );
}

export default Dashboard;
