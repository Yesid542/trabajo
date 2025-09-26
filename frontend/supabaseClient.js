import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://mebggeuawlwhwytjcyek.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1lYmdnZXVhd2x3aHd5dGpjeWVrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY3NDQxMDMsImV4cCI6MjA3MjMyMDEwM30.sjfBMnNDwjZTdMLacUW0TOwxqnU0OPtcVIf01PugwBc'

export const supabase = createClient(supabaseUrl, supabaseKey)