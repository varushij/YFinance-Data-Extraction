------------------------------------------------
--One time script to create tables in Postgres
------------------------------------------------

---Every 5 minutes data
CREATE TABLE public.forex_5min
(
    ticker text NOT NULL,
    datetime timestamp with time zone NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    adj_close double precision,
    volume bigint,
    timeframe character varying,
    PRIMARY KEY (ticker, datetime)
);

--Every 15 minutes data
CREATE TABLE public.forex_15min
(
    ticker text NOT NULL,
    datetime timestamp with time zone NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    adj_close double precision,
    volume bigint,
    timeframe character varying,
    PRIMARY KEY (ticker, datetime)
);

--Every 30 minutes data
CREATE TABLE public.forex_30min
(
    ticker text NOT NULL,
    datetime timestamp with time zone NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    adj_close double precision,
    volume bigint,
    timeframe character varying,
    PRIMARY KEY (ticker, datetime)
);

--Every 60 minutes data
CREATE TABLE public.forex_60min
(
    ticker text NOT NULL,
    datetime timestamp with time zone NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    adj_close double precision,
    volume bigint,
    timeframe character varying,
    PRIMARY KEY (ticker, datetime)
);

-- Every 240 minutes data
CREATE TABLE public.forex_240min
(
    ticker text NOT NULL,
    datetime timestamp with time zone NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    adj_close double precision,
    volume bigint,
    timeframe character varying,
    PRIMARY KEY (ticker, datetime)
);

-- Everyday data
CREATE TABLE public.forex_daily
(
    ticker text NOT NULL,
    date date NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    adj_close double precision,
    volume bigint,
    timeframe character varying,
    PRIMARY KEY (ticker, date)
);

-- Every week data
CREATE TABLE public.forex_weekly
(
    ticker text NOT NULL,
    date date NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    adj_close double precision,
    volume bigint,
    timeframe character varying,
    PRIMARY KEY (ticker, date)
);

-- Every month data
CREATE TABLE public.forex_monthly
(
    ticker text NOT NULL,
    date date NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    adj_close double precision,
    volume bigint,
    timeframe character varying,
    PRIMARY KEY (ticker, date)
);