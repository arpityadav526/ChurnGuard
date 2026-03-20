import { createBrowserRouter } from "react-router";
import { LoginPage } from "./pages/LoginPage";
import { Dashboard } from "./pages/Dashboard";
import { PredictCustomer } from "./pages/PredictCustomer";
import { Insights } from "./pages/Insights";
import { RetentionStrategy } from "./pages/RetentionStrategy";
import { Reports } from "./pages/Reports";
import { Settings } from "./pages/Settings";
import { NotFound } from "./pages/NotFound";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: LoginPage,
  },
  {
    path: "/dashboard",
    Component: Dashboard,
  },
  {
    path: "/predict",
    Component: PredictCustomer,
  },
  {
    path: "/insights",
    Component: Insights,
  },
  {
    path: "/retention",
    Component: RetentionStrategy,
  },
  {
    path: "/reports",
    Component: Reports,
  },
  {
    path: "/settings",
    Component: Settings,
  },
  {
    path: "*",
    Component: NotFound,
  },
]);