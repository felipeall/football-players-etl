SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.seasons DROP CONSTRAINT IF EXISTS seasons_pk;
ALTER TABLE IF EXISTS ONLY public.players DROP CONSTRAINT IF EXISTS players_pk;
ALTER TABLE IF EXISTS ONLY public.matches_statistics DROP CONSTRAINT IF EXISTS matches_statistics_pk;
ALTER TABLE IF EXISTS ONLY public.competitions DROP CONSTRAINT IF EXISTS competitions_pk;
DROP TABLE IF EXISTS public.seasons;
DROP TABLE IF EXISTS public.players;
DROP TABLE IF EXISTS public.matches_statistics;
DROP TABLE IF EXISTS public.competitions;
-- *not* dropping schema, since initdb creates it
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: competitions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.competitions (
    id text NOT NULL,
    name text,
    gender text,
    "category.id" text,
    "category.name" text,
    "category.country_code" text,
    parent_id text
);


ALTER TABLE public.competitions OWNER TO postgres;

--
-- Name: matches_statistics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.matches_statistics (
    id text NOT NULL,
    start_time timestamp with time zone,
    competitors_id text,
    competitors_qualifier text,
    players_id text NOT NULL,
    players_name text,
    players_starter boolean,
    assists double precision,
    chances_created double precision,
    clearances double precision,
    crosses_successful double precision,
    crosses_total double precision,
    defensive_blocks double precision,
    diving_saves double precision,
    dribbles_completed double precision,
    fouls_committed double precision,
    goals_by_head double precision,
    goals_by_penalty double precision,
    goals_conceded double precision,
    goals_scored double precision,
    interceptions double precision,
    long_passes_successful double precision,
    long_passes_total double precision,
    long_passes_unsuccessful double precision,
    loss_of_possession double precision,
    minutes_played double precision,
    own_goals double precision,
    passes_successful double precision,
    passes_total double precision,
    passes_unsuccessful double precision,
    penalties_faced double precision,
    penalties_missed double precision,
    penalties_saved double precision,
    red_cards double precision,
    shots_faced_saved double precision,
    shots_faced_total double precision,
    substituted_in double precision,
    substituted_out double precision,
    tackles_successful double precision,
    tackles_total double precision,
    was_fouled double precision,
    yellow_cards double precision,
    yellow_red_cards double precision,
    shots_off_target double precision,
    shots_on_target double precision,
    corner_kicks double precision,
    offsides double precision,
    shots_blocked double precision,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.matches_statistics OWNER TO postgres;

--
-- Name: players; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.players (
    id text NOT NULL,
    name text,
    type text,
    date_of_birth timestamp without time zone,
    nationality text,
    country_code text,
    height double precision,
    weight double precision,
    jersey_number double precision,
    preferred_foot text,
    place_of_birth text,
    nickname text,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.players OWNER TO postgres;

--
-- Name: seasons; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seasons (
    id text NOT NULL,
    name text,
    start_date text,
    end_date text,
    year text,
    competition_id text
);


ALTER TABLE public.seasons OWNER TO postgres;