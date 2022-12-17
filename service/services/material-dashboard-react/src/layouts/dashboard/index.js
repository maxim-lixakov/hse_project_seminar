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
// import reportsLineChartData from "layouts/dashboard/data/reportsLineChartData";

// Dashboard components
import Projects from "layouts/dashboard/components/Projects";
import OrdersOverview from "layouts/dashboard/components/OrdersOverview";

function Dashboard() {
  // const { sales, tasks } = reportsLineChartData;
  const [records_amt, setRecordsAmt] = useState("");
  const [last_qty, setLastQty] = useState("");
  const [qty_values, setQtyValues] = useState("");
  const [qty_growth, setQtyGrowth] = useState("");
  const [revenue_week_growth_rate, setRevenueWeekGrowthRate] = useState("");
  const [predicted_revenue_values, setPredictedRevenueValues] = useState("");
  const [revenue_values, setRevenueValues] = useState("");
  useEffect(() => {
    // const url = "http://localhost:1337/api/data_info";
    // const fetchData2 = async () => {
    //   try {
    //     const response = await fetch(url);
    //     const json = await response.json();
    //     setRows(json.rows);
    //   } catch (error) {
    //     console.log("error", error);
    //   }
    // };
    const fetchData = async () => {
      try {
        console.log(good_id, good_id.toString())
        const  url = `http://217.25.88.87:1337/api/info/${good_id.good_id}`;
        const response = await fetch(url);
        const json = await response.json();
        let qty_values = json.qty_values;
        let last_qty = json.last_qty;
        setRecordsAmt(json.records_amt)
        setQtyGrowth(`${json.qty_growth}%`);
        setRevenueWeekGrowthRate(`${json.revenue_week_growth_rate}%`)
        setLastQty(last_qty);
        setPredictedRevenueValues({
      labels: ["M", "T", "W", "T", "F", "S", "S"],
    datasets: { label: "предсказуемая выручка (руб)", data: json.predicted_revenue_values.slice(-7)},
  });
        setRevenueValues({
      labels: ["M", "T", "W", "T", "F", "S", "S"],
    datasets: { label: "выручка (руб)", data: json.revenue_values.slice(-7)},
  })
        setQtyValues({
  labels: ["M", "T", "W", "T", "F", "S", "S"],
  datasets: { label: "кол-во товара", data: qty_values.slice(-7)},
});
      } catch (error) {
        console.log("error", error);
      }
    };
    // fetchData2();
    fetchData()
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
                count={records_amt}
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                icon="leaderboard"
                title="Кол-во товара на складе"
                count={last_qty}
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="success"
                icon="store"
                title="Прирост кол-ва товара"
                count={qty_growth}
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="primary"
                icon="person_add"
                title="Прирост выручки"
                count={revenue_week_growth_rate}
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
                  date="обновлено 21.12.2022"
                  chart={qty_values}
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
                      (<strong>+{revenue_week_growth_rate}</strong>) прирост выручки.
                    </>
                  }
                  date="обновлено 21.12.2022"
                  chart={revenue_values}
                />
              </MDBox>
            </Grid>
            <Grid item xs={12} md={6} lg={4}>
              <MDBox mb={3}>
                <ReportsLineChart
                  color="dark"
                  title="Прогноз выручки"
                  description="ожидаемый прогноз выручки на 7 дней"
                  date="обновлено 21.12.2022"
                  chart={predicted_revenue_values}
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
