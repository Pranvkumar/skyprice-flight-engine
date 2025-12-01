import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: `${API_URL}/api/v1` }),
  tagTypes: ['Flights', 'Forecasts', 'Analytics'],
  endpoints: (builder) => ({
    searchFlights: builder.query({
      query: (params) => ({
        url: '/flights/search',
        params,
      }),
      providesTags: ['Flights'],
    }),
    predictPrice: builder.mutation({
      query: (body) => ({
        url: '/forecast/predict',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['Forecasts'],
    }),
    getAnalyticsDashboard: builder.query({
      query: () => '/analytics/dashboard',
      providesTags: ['Analytics'],
    }),
    getPriceTrends: builder.query({
      query: (params) => ({
        url: '/analytics/trends',
        params,
      }),
      providesTags: ['Analytics'],
    }),
  }),
});

export const {
  useSearchFlightsQuery,
  usePredictPriceMutation,
  useGetAnalyticsDashboardQuery,
  useGetPriceTrendsQuery,
} = apiSlice;
