import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from './ui/dropdown-menu'
import { LogOutIcon, UserPen } from 'lucide-react'
import { Avatar, AvatarFallback } from './ui/avatar'
import { Button } from './ui/button'
import { useAuthStore } from '@/store/auth-store'
import { useQuery } from '@tanstack/react-query'
import { userOptions } from '@/queries/user.queries'
import { Skeleton } from './ui/skeleton'
import { Link } from 'react-router'
import { ROUTES } from '@/lib/constants'

export function AccountMenu({ isAuthenticated }: { isAuthenticated: boolean }) {
  const logout = useAuthStore(s => s.logout)
  const { data, isLoading, isError } = useQuery(userOptions(isAuthenticated))
  return (
    <>
      {isLoading || isError || !data ? (
        <Skeleton className='size-9 rounded-full' />
      ) : (
        <DropdownMenu>
          <DropdownMenuTrigger
            render={
              <Button variant='ghost' size='icon-lg' className='rounded-full'>
                <Avatar className='size-9'>
                  <AvatarFallback>
                    {data.first_name[0]}
                    {data.last_name[0]}
                  </AvatarFallback>
                </Avatar>
              </Button>
            }
          />
          <DropdownMenuContent align='end' sideOffset={2}>
            <DropdownMenuItem render={<Link to={ROUTES.profile} />}>
              <UserPen />
              Ver perfil
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => logout()} variant='destructive'>
              <LogOutIcon />
              Log out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )}
    </>
  )
}
