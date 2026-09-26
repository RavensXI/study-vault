-- Rollback for 20260926120000_answer_pool.sql
drop function if exists public.pool_add(jsonb);
drop table if exists public.answer_pool;
